const fs = require('fs');
const path = require('path');

const extensionRoot = path.resolve(__dirname, '..');
const projectRoot = path.resolve(extensionRoot, '..');
const bundleRoot = path.join(extensionRoot, 'python-src');

function resetDir(targetPath) {
  fs.rmSync(targetPath, { recursive: true, force: true });
  fs.mkdirSync(targetPath, { recursive: true });
}

function copyDir(sourceDir, targetDir) {
  fs.mkdirSync(targetDir, { recursive: true });
  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    if (entry.name === '__pycache__' || entry.name.endsWith('.pyc') || entry.name.endsWith('.pyo')) {
      continue;
    }

    const sourcePath = path.join(sourceDir, entry.name);
    const targetPath = path.join(targetDir, entry.name);

    if (entry.isDirectory()) {
      copyDir(sourcePath, targetPath);
      continue;
    }

    fs.copyFileSync(sourcePath, targetPath);
  }
}

function main() {
  resetDir(bundleRoot);

  copyDir(path.join(projectRoot, 'main'), path.join(bundleRoot, 'main'));
  fs.mkdirSync(path.join(bundleRoot, 'dom'), { recursive: true });
  fs.copyFileSync(path.join(projectRoot, 'dom', 'dom.py'), path.join(bundleRoot, 'dom', 'dom.py'));
  fs.writeFileSync(path.join(bundleRoot, 'dom', '__init__.py'), '');
}

main();
