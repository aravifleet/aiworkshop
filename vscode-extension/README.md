# Adaptive QA Story Runner

This VS Code extension bundles the markdown-driven adaptive QA runtime so teams can install a `.vsix`, paste a story `.md` file into any workspace, and run the workflow from VS Code.

## What Users Do

1. Install the `.vsix` in VS Code.
2. Open any workspace folder.
3. Run `Adaptive QA: Start` and choose:
   - `Import Markdown File`
   - or `Paste Story Text`
4. The extension opens the story and immediately starts the workflow for that file.
5. Run `Adaptive QA: Install Playwright Browser` once on a new machine if Playwright browsers are not installed yet.

The extension starts the selected workflow in a VS Code terminal and sets `USER_STORY_FILE` automatically.

## Commands

- `Adaptive QA: Start`
- `Adaptive QA: Add Story`
- `Adaptive QA: Run Active Story`
- `Adaptive QA: Pick Story and Run`
- `Adaptive QA: Create Story Template`
- `Adaptive QA: Install Playwright Browser`

## Supported Workflows

- `Guided Checkout Flow`
  - Runs the bundled multi-preference guided checkout flow
- `Adaptive Discovery Only`
  - Runs the bundled adaptive discovery flow

## Package as VSIX

From `vscode-extension/`:

```powershell
npm install
npm run package
```

That generates a `.vsix` file that can be shared with clients.
