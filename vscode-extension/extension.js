const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

function isPathLike(command) {
  return path.isAbsolute(command) || command.includes(path.sep) || /^[A-Za-z]:/.test(command);
}

function escapePowerShell(value) {
  return String(value).replace(/'/g, "''");
}

function escapeBash(value) {
  return String(value).replace(/'/g, `'\\''`);
}

function resolveLaunchSpec(configuredPythonPath) {
  if (configuredPythonPath && configuredPythonPath.trim()) {
    return {
      command: configuredPythonPath.trim(),
      source: 'configured',
    };
  }

  return {
    command: process.platform === 'win32' ? 'python' : 'python3',
    source: 'system-default',
  };
}

function buildTerminalCommand(spec, runnerPath, filePath, extraArgs = '') {
  const hasPathLikeCommand = isPathLike(spec.command);

  if (process.platform === 'win32') {
    const pythonCommand = escapePowerShell(spec.command);
    const runner = escapePowerShell(runnerPath);
    const fileArg = filePath ? ` --file '${escapePowerShell(filePath)}'` : '';
    const runCommand = `& '${pythonCommand}' '${runner}'${fileArg}${extraArgs}`;
    const guidance = [
      "Write-Host 'Agentic-QA requires Python 3.9+ on this machine.' -ForegroundColor Yellow",
      "Write-Host 'Install Python, then run these commands:' -ForegroundColor Yellow",
      "Write-Host 'python -m pip install groq playwright PyPDF2 python-docx' -ForegroundColor Cyan",
      "Write-Host 'python -m playwright install' -ForegroundColor Cyan",
    ].join('; ');

    if (hasPathLikeCommand) {
      return `if (Test-Path '${pythonCommand}') { ${runCommand} } else { ${guidance} }`;
    }

    return `$agenticQaPython = Get-Command '${pythonCommand}' -ErrorAction SilentlyContinue; if ($agenticQaPython) { ${runCommand} } else { ${guidance} }`;
  }

  const pythonCommand = escapeBash(spec.command);
  const runner = escapeBash(runnerPath);
  const fileArg = filePath ? ` --file '${escapeBash(filePath)}'` : '';
  const runCommand = `'${pythonCommand}' '${runner}'${fileArg}${extraArgs}`;
  const guidance = [
    "echo 'Agentic-QA requires Python 3.9+ on this machine.'",
    "echo 'Install Python, then run these commands:'",
    "echo 'python3 -m pip install groq playwright PyPDF2 python-docx'",
    "echo 'python3 -m playwright install'",
  ].join('; ');

  if (hasPathLikeCommand) {
    return `if [ -x '${pythonCommand}' ]; then ${runCommand}; else ${guidance}; fi`;
  }

  return `if command -v '${pythonCommand}' >/dev/null 2>&1; then ${runCommand}; else ${guidance}; fi`;
}

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const runWithMode = async (mode) => {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) {
      vscode.window.showErrorMessage('Open a workspace folder before running Agentic QA.');
      return;
    }

    const workspacePath = folders[0].uri.fsPath;
    const config = vscode.workspace.getConfiguration('agenticQA');
    const configuredPythonPath = config.get('pythonPath');
    const extensionPath = context.extensionPath;
    const runnerPath = path.join(extensionPath, 'runner.py');
    const launchSpec = resolveLaunchSpec(configuredPythonPath);

    if (!fs.existsSync(runnerPath)) {
      vscode.window.showErrorMessage('The bundled Agentic-QA runner is missing from this VSIX. Rebuild the extension package and reinstall it.');
      return;
    }

    const choice = await vscode.window.showQuickPick(['Upload file', 'Paste scenario'], {
      placeHolder: 'Choose how to provide the test scenario',
    });
    if (!choice) {
      return;
    }

    const modeArgs = mode === 'teach' ? ' --teach' : '';
    let command = buildTerminalCommand(launchSpec, runnerPath, undefined, modeArgs);
    if (choice === 'Upload file') {
      const fileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        filters: { 'Instructions': ['txt', 'md', 'pdf', 'docx', 'csv'] },
        openLabel: 'Select instruction file',
      });
      if (!fileUri || fileUri.length === 0) {
        return;
      }
      command = buildTerminalCommand(launchSpec, runnerPath, fileUri[0].fsPath, modeArgs);
    } else if (choice === 'Paste scenario') {
      const scenarioText = await vscode.window.showInputBox({
        prompt: 'Paste the full scenario text, starting with the URL on the first line.',
        placeHolder: 'https://example.com\nUsername: user\nPassword: pass\nVerify login works.',
        validateInput: value => value && value.trim() ? null : 'Scenario text is required',
        ignoreFocusOut: true,
      });
      if (!scenarioText) {
        return;
      }
      const docsPath = path.join(workspacePath, 'docsnew');
      if (!fs.existsSync(docsPath)) {
        fs.mkdirSync(docsPath, { recursive: true });
      }
      const fileName = 'pasted_scenario.md';
      const filePath = path.join(docsPath, fileName);
      fs.writeFileSync(filePath, scenarioText, { encoding: 'utf8' });
      command = buildTerminalCommand(launchSpec, runnerPath, filePath, modeArgs);
    }

    const terminal = vscode.window.createTerminal({ name: mode === 'teach' ? 'Agentic QA Teach' : 'Agentic QA', cwd: workspacePath });
    terminal.show();
    terminal.sendText(command);
    if (mode === 'teach') {
      vscode.window.showInformationMessage('Agentic-QA teach mode started in the terminal. Manually explore in the opened browser, then press Enter in the terminal to save learned patterns.');
    } else {
      vscode.window.showInformationMessage('Agentic-QA started in the terminal. Approve the generated use cases there to continue the run.');
    }
  };

  const disposable = vscode.commands.registerCommand('agenticQA.run', async () => runWithMode('run'));
  const teachDisposable = vscode.commands.registerCommand('agenticQA.teach', async () => runWithMode('teach'));

  context.subscriptions.push(disposable);
  context.subscriptions.push(teachDisposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
