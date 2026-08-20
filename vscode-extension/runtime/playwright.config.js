const path = require('node:path');
const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: path.join(__dirname, 'adaptive-checkout'),
  fullyParallel: false,
  workers: 1,
  retries: 0,
  use: {
    ...devices['Desktop Chrome'],
    headless: false,
    launchOptions: {
      slowMo: 250
    }
  },
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome']
      }
    }
  ]
});
