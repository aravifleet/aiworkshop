const fs = require('fs');
const path = require('path');
const vscode = require('vscode');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
  const disposable = vscode.commands.registerCommand('agenticQA.run', async () => {
    const folders = vscode.workspace.workspaceFolders;
    if (!folders || folders.length === 0) {
      vscode.window.showErrorMessage('Open a workspace folder before running Agentic QA.');
      return;
    }

    const workspacePath = folders[0].uri.fsPath;
    const config = vscode.workspace.getConfiguration('agenticQA');
    const configuredPythonPath = config.get('pythonPath');
    const pythonPath = configuredPythonPath && configuredPythonPath.trim()
      ? configuredPythonPath.trim()
      : (process.platform === 'win32' ? 'python' : 'python3');
    const extensionPath = context.extensionPath;
    const runnerPath = path.join(extensionPath, 'runner.py');

    const choice = await vscode.window.showQuickPick(['Upload file', 'Paste scenario'], {
      placeHolder: 'Choose how to provide the test scenario',
    });
    if (!choice) {
      return;
    }

    let command = `${pythonPath} "${runnerPath}"`;
    if (choice === 'Upload file') {
      const fileUri = await vscode.window.showOpenDialog({
        canSelectMany: false,
        filters: { 'Instructions': ['txt', 'md', 'pdf', 'docx'] },
        openLabel: 'Select instruction file',
      });
      if (!fileUri || fileUri.length === 0) {
        return;
      }
      command = `${pythonPath} "${runnerPath}" --file "${fileUri[0].fsPath}"`;
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
      command = `${pythonPath} "${runnerPath}" --file "${filePath}"`;
    }

    const terminal = vscode.window.createTerminal({ name: 'Agentic QA', cwd: workspacePath });
    terminal.show();
    terminal.sendText(command);
    vscode.window.showInformationMessage('Agentic-QA started in the terminal. Approve the generated use cases there to continue the run.');
  });

  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate,
};
