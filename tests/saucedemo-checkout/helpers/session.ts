import { expect, type Page } from '@playwright/test';

import { BASE_URL, USERS } from '../test-data';

export async function gotoLogin(page: Page) {
  await page.goto(BASE_URL, { waitUntil: 'domcontentloaded' });
  await expect(page).toHaveURL(/saucedemo\.com\/?$/);
}

export async function login(page: Page) {
  await gotoLogin(page);
  await page.locator('[data-test="username"]').fill(USERS.standard.username);
  await page.locator('[data-test="password"]').fill(USERS.standard.password);
  await page.locator('[data-test="login-button"]').click();
  await expect(page).toHaveURL(/inventory\.html$/);
}

export async function logout(page: Page) {
  await page.locator('#react-burger-menu-btn').click();
  await page.locator('[data-test="logout-sidebar-link"]').click();
  await expect(page).toHaveURL(/saucedemo\.com\/?$/);
}
