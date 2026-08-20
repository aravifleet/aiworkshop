const vscode = require('vscode');
const fs = require('node:fs');
const path = require('node:path');

const EXTENSION_OUTPUT = 'Adaptive QA Story Runner';

function getOutputChannel() {
  return vscode.window.createOutputChannel(EXTENSION_OUTPUT);
}

function getWorkspaceRoot() {
  const folder = vscode.workspace.workspaceFolders?.[0];
  return folder?.uri.fsPath ?? null;
}

function isMarkdownStory(filePath) {
  return filePath.toLowerCase().endsWith('.md');
}

function normalizeRelativeStoryPath(workspaceRoot, filePath) {
  return path.relative(workspaceRoot, filePath).replace(/\\/g, '/');
}

function quoteForShell(value) {
  return `"${String(value).replace(/"/g, '\\"')}"`;
}

function getRuntimePath(context, ...segments) {
  return path.join(context.extensionPath, 'runtime', ...segments);
}

function getBundledPlaywrightCommand(context) {
  const cliPath = path.join(context.extensionPath, 'node_modules', 'playwright', 'cli.js');
  return `node ${quoteForShell(cliPath)}`;
}

function getPlaywrightCliCommand(context) {
  const config = vscode.workspace.getConfiguration('adaptiveQa');
  return config.get('playwrightCommand', '').trim() || getBundledPlaywrightCommand(context);
}

async function chooseWorkflow() {
  const config = vscode.workspace.getConfiguration('adaptiveQa');
  const defaultWorkflow = config.get('defaultWorkflow', 'guided');
  const picked = await vscode.window.showQuickPick(
    [
      {
        label: 'Guided Checkout Flow',
        description: 'Runs the story-driven multi-preference guided checkout flow.',
        workflow: 'guided'
      },
      {
        label: 'Adaptive Discovery Only',
        description: 'Discovers routes, selectors, and gaps without completing the full journey.',
        workflow: 'discovery'
      }
    ],
    {
      placeHolder: `Choose a workflow for this story. Default: ${defaultWorkflow}`
    }
  );

  return picked?.workflow ?? null;
}

function getCommandForWorkflow(context, workflow, browserProject) {
  const configPath = getRuntimePath(context, 'playwright.config.js');

  if (workflow === 'discovery') {
    return `test -c ${quoteForShell(configPath)} adaptive-checkout.spec.ts --project=${browserProject} --workers=1 --reporter=line`;
  }

  return `test -c ${quoteForShell(configPath)} pantheon-guided-checkout.spec.ts --project=${browserProject} --workers=1 --reporter=line`;
}

async function runStory(context, workspaceRoot, storyPath) {
  if (!workspaceRoot) {
    vscode.window.showErrorMessage('Open a workspace folder before running a story.');
    return;
  }

  if (!fs.existsSync(storyPath)) {
    vscode.window.showErrorMessage(`Story file not found: ${storyPath}`);
    return;
  }

  if (!isMarkdownStory(storyPath)) {
    vscode.window.showErrorMessage('Please choose a markdown story file.');
    return;
  }

  const workflow = await chooseWorkflow();
  if (!workflow) {
    return;
  }

  const config = vscode.workspace.getConfiguration('adaptiveQa');
  const browserProject = config.get('browserProject', 'chromium');
  const relativeStoryPath = normalizeRelativeStoryPath(workspaceRoot, storyPath);
  const output = getOutputChannel();
  const commandArgs = getCommandForWorkflow(context, workflow, browserProject);
  const shellCommand = `${getPlaywrightCliCommand(context)} ${commandArgs}`;

  output.show(true);
  output.clear();
  output.appendLine(`Workspace: ${workspaceRoot}`);
  output.appendLine(`Story: ${relativeStoryPath}`);
  output.appendLine(`Workflow: ${workflow}`);
  output.appendLine(`Command: ${shellCommand}`);
  output.appendLine('');

  const terminal = vscode.window.createTerminal({
    name: `Adaptive QA: ${path.basename(storyPath)}`,
    cwd: workspaceRoot,
    env: {
      USER_STORY_FILE: storyPath
    }
  });

  terminal.show(true);
  terminal.sendText(shellCommand, true);

  vscode.window.showInformationMessage(
    `Started ${workflow} workflow for ${path.basename(storyPath)} in a VS Code terminal.`
  );
}

async function getActiveStoryPath(uri) {
  if (uri?.fsPath) {
    return uri.fsPath;
  }

  const editorPath = vscode.window.activeTextEditor?.document?.uri?.fsPath;
  if (editorPath && isMarkdownStory(editorPath)) {
    return editorPath;
  }

  return null;
}

async function pickStoryFile(workspaceRoot) {
  const stories = await vscode.workspace.findFiles('**/*.md', '**/{node_modules,.git}/**');
  if (stories.length === 0) {
    vscode.window.showErrorMessage('No markdown story files were found in the current workspace.');
    return null;
  }

  const picked = await vscode.window.showQuickPick(
    stories.map((uri) => ({
      label: path.basename(uri.fsPath),
      description: normalizeRelativeStoryPath(workspaceRoot, uri.fsPath),
      fsPath: uri.fsPath
    })),
    {
      placeHolder: 'Choose a markdown story to run'
    }
  );

  return picked?.fsPath ?? null;
}

async function createStoryTemplate() {
  const workspaceRoot = getWorkspaceRoot();
  if (!workspaceRoot) {
    vscode.window.showErrorMessage('Open the project folder before creating a story template.');
    return;
  }

  const storiesDir = path.join(workspaceRoot, 'user-stories');
  fs.mkdirSync(storiesDir, { recursive: true });

  const templatePath = path.join(storiesDir, 'client-workflow-template.md');
  if (!fs.existsSync(templatePath)) {
    const template = `# User Story: CLIENT-001 - Adaptive Workflow

## Application URL

https://example.com

## Test Credentials

- Username: user@example.com
- Password: Password123

## Business Objective

Describe the business goal this workflow should validate.

## Acceptance Criteria

### AC1: Login

- GIVEN I am a valid user
- WHEN I open the application
- THEN I should be able to authenticate successfully

### AC2: Journey Execution

- GIVEN I am authenticated
- WHEN I follow the configured journey steps
- THEN I should reach the configured stop point or complete the flow successfully

## Journey Notes

- Use adaptive selector discovery.
- Prefer live UI behavior over hardcoded selectors.
- Log gaps if the website behavior differs from the story.

## Checkout Preferences

Repeat this block as Checkout Preference 1, 2, 3, and so on when the website supports multiple shipping or payment paths.

### Checkout Preference 1

- Name: Example preference
- Product Selection: First purchasable product
- Address Strategy: Random US address
- Shipping Method: Any
- Payment Method: House Account
- Payment Detail: Random
- Review Before Purchase: Yes
- Complete Purchase: Yes
- Stop After: purchase
`;

    fs.writeFileSync(templatePath, template, 'utf8');
  }

  const document = await vscode.workspace.openTextDocument(templatePath);
  await vscode.window.showTextDocument(document);
  vscode.window.showInformationMessage('Created a reusable story template under user-stories/.');
}

async function ensureStoriesDir(workspaceRoot) {
  const storiesDir = path.join(workspaceRoot, 'user-stories');
  fs.mkdirSync(storiesDir, { recursive: true });
  return storiesDir;
}

async function importStoryFile(workspaceRoot) {
  const picked = await vscode.window.showOpenDialog({
    canSelectFiles: true,
    canSelectFolders: false,
    canSelectMany: false,
    filters: {
      Markdown: ['md']
    },
    openLabel: 'Import Story File'
  });

  if (!picked?.length) {
    return null;
  }

  const sourcePath = picked[0].fsPath;
  const storiesDir = await ensureStoriesDir(workspaceRoot);
  const targetPath = path.join(storiesDir, path.basename(sourcePath));

  fs.copyFileSync(sourcePath, targetPath);
  return targetPath;
}

async function pasteStoryIntoFile(workspaceRoot) {
  const fileName =
    (await vscode.window.showInputBox({
      title: 'Adaptive QA Story',
      prompt: 'Enter a file name for the pasted story',
      placeHolder: 'client-story.md',
      value: 'client-story.md',
      validateInput: (value) => {
        const trimmed = value.trim();
        if (!trimmed) {
          return 'File name is required.';
        }
        if (!trimmed.toLowerCase().endsWith('.md')) {
          return 'Use a .md file name.';
        }
        return null;
      }
    })) ?? '';

  if (!fileName.trim()) {
    return null;
  }

  const storyText =
    (await vscode.window.showInputBox({
      title: 'Paste Story Markdown',
      prompt: 'Paste the full markdown story content',
      placeHolder: '# User Story: ...',
      ignoreFocusOut: true
    })) ?? '';

  if (!storyText.trim()) {
    return null;
  }

  const storiesDir = await ensureStoriesDir(workspaceRoot);
  const targetPath = path.join(storiesDir, fileName.trim());
  fs.writeFileSync(targetPath, storyText, 'utf8');
  return targetPath;
}

async function addStoryToWorkspace(context) {
  const workspaceRoot = getWorkspaceRoot();
  if (!workspaceRoot) {
    vscode.window.showErrorMessage('Open a workspace folder before adding a story.');
    return;
  }

  const choice = await vscode.window.showQuickPick(
    [
      {
        label: 'Import Markdown File',
        description: 'Choose an existing .md story file from your machine.',
        mode: 'import'
      },
      {
        label: 'Paste Story Text',
        description: 'Paste the markdown story content and save it into this workspace.',
        mode: 'paste'
      }
    ],
    {
      placeHolder: 'How do you want to add the story?'
    }
  );

  if (!choice) {
    return;
  }

  const storyPath =
    choice.mode === 'import'
      ? await importStoryFile(workspaceRoot)
      : await pasteStoryIntoFile(workspaceRoot);

  if (!storyPath) {
    return;
  }

  const document = await vscode.workspace.openTextDocument(storyPath);
  await vscode.window.showTextDocument(document);
  vscode.window.showInformationMessage(`Story ready: ${path.basename(storyPath)}. Starting workflow...`);
  await runStory(context, workspaceRoot, storyPath);
}

async function quickStart(context) {
  await addStoryToWorkspace(context);
}

async function installBrowsers(context) {
  const workspaceRoot = getWorkspaceRoot();
  if (!workspaceRoot) {
    vscode.window.showErrorMessage('Open a workspace folder before installing Playwright browsers.');
    return;
  }

  const config = vscode.workspace.getConfiguration('adaptiveQa');
  const browserProject = config.get('browserProject', 'chromium');
  const shellCommand = `${getPlaywrightCliCommand(context)} install ${browserProject}`;
  const output = getOutputChannel();

  output.show(true);
  output.clear();
  output.appendLine(`Workspace: ${workspaceRoot}`);
  output.appendLine(`Command: ${shellCommand}`);
  output.appendLine('');

  const terminal = vscode.window.createTerminal({
    name: `Adaptive QA: Install ${browserProject}`,
    cwd: workspaceRoot
  });

  terminal.show(true);
  terminal.sendText(shellCommand, true);

  vscode.window.showInformationMessage(
    `Started Playwright browser install for ${browserProject} in a VS Code terminal.`
  );
}

function activate(context) {
  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.runActiveStory', async (uri) => {
      const workspaceRoot = getWorkspaceRoot();
      const storyPath = await getActiveStoryPath(uri);

      if (!storyPath) {
        vscode.window.showErrorMessage('Open a markdown story file or right-click one in the explorer.');
        return;
      }

      await runStory(context, workspaceRoot, storyPath);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.pickStoryAndRun', async () => {
      const workspaceRoot = getWorkspaceRoot();
      if (!workspaceRoot) {
        vscode.window.showErrorMessage('Open the project folder before picking a story.');
        return;
      }

      const storyPath = await pickStoryFile(workspaceRoot);
      if (!storyPath) {
        return;
      }

      await runStory(context, workspaceRoot, storyPath);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.generateStoryTemplate', async () => {
      await createStoryTemplate();
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.addStory', async () => {
      await addStoryToWorkspace(context);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.quickStart', async () => {
      await quickStart(context);
    })
  );

  context.subscriptions.push(
    vscode.commands.registerCommand('adaptiveQa.installBrowsers', async () => {
      await installBrowsers(context);
    })
  );
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
