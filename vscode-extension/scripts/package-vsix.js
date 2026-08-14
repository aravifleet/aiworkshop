const childProcess = require('child_process');
const fs = require('fs');
const path = require('path');

const extensionRoot = path.resolve(__dirname, '..');

function resolveVsceCommand() {
  const localBin = process.platform === 'win32'
    ? path.join(extensionRoot, 'node_modules', '.bin', 'vsce.cmd')
    : path.join(extensionRoot, 'node_modules', '.bin', 'vsce');

  if (fs.existsSync(localBin)) {
    return {
      command: process.platform === 'win32' ? 'npx.cmd' : 'npx',
      args: ['--no-install', '@vscode/vsce', 'package'],
      shell: process.platform === 'win32',
    };
  }

  const globalCommand = process.platform === 'win32' ? 'vsce.cmd' : 'vsce';
  const probe = childProcess.spawnSync(globalCommand, ['--version'], {
    cwd: extensionRoot,
    encoding: 'utf8',
    shell: false,
    windowsHide: true,
  });

  if (!probe.error && probe.status === 0) {
    return {
      command: globalCommand,
      args: ['package'],
      shell: process.platform === 'win32',
    };
  }

  throw new Error(
    "VS Code Extension packaging tool 'vsce' was not found. Install '@vscode/vsce' on the packaging machine, then run 'npm run vsix:package' again."
  );
}

function main() {
  const { command, args, shell = false } = resolveVsceCommand();
  const result = childProcess.spawnSync(command, args, {
    cwd: extensionRoot,
    stdio: 'inherit',
    shell,
    windowsHide: false,
  });

  if (result.error) {
    throw result.error;
  }

  process.exit(result.status || 0);
}

main();
