import { expect, test } from '@playwright/test';

import { discoverAdaptiveCheckoutProfile, type AppProfile } from './discovery';
import { readStoryConfig, type StoryConfig } from './story';

let story: StoryConfig;
let profile: AppProfile;

test.describe.serial('Adaptive checkout discovery', () => {
  test.beforeAll(async ({ browser }, testInfo) => {
    testInfo.setTimeout(120000);
    story = readStoryConfig();
    profile = await discoverAdaptiveCheckoutProfile(browser, story);
  });

  test('discovers the app shell from the current story target', async () => {
    expect(profile.story.baseUrl).toBe(story.baseUrl);
    expect(profile.home.title.length).toBeGreaterThan(0);
    expect(profile.home.loginHref || profile.login.url).toBeTruthy();
    expect(profile.home.cartHref || profile.cart.url).toBeTruthy();
  });

  test('maps the live login flow and validates story credentials', async () => {
    expect(profile.login.usernameSelector).toBeTruthy();
    expect(profile.login.passwordSelector).toBeTruthy();
    expect(profile.login.submitSelector).toBeTruthy();
    expect(profile.capabilities.login).toBeTruthy();
  });

  test('discovers a live product page and add-to-cart control', async () => {
    expect(profile.product.url).toBeTruthy();
    expect(profile.product.title).toBeTruthy();
    expect(profile.product.addToCartSelector).toBeTruthy();
  });

  test('discovers the cart and checkout entry point', async () => {
    expect(profile.capabilities.cartAccess).toBeTruthy();
    expect(profile.cart.url).toBeTruthy();
    expect(profile.cart.checkoutSelector).toBeTruthy();
  });

  test('writes a dynamic gap report for story vs app mismatches', async ({}, testInfo) => {
    expect(profile.artifacts.profilePath).toBeTruthy();
    expect(profile.artifacts.gapReportPath).toBeTruthy();

    await testInfo.attach('discovered-gaps', {
      body: profile.gaps.length === 0 ? 'No gaps detected.' : profile.gaps.join('\n'),
      contentType: 'text/plain',
    });
  });
});
