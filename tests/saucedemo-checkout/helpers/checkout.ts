import { expect, type Page } from '@playwright/test';

export async function addItemToCart(page: Page, itemName: string) {
  const item = page.locator('.inventory_item').filter({ hasText: itemName });
  await item.getByRole('button', { name: 'Add to cart' }).click();
}

export async function addItemsToCart(page: Page, itemNames: string[]) {
  for (const itemName of itemNames) {
    await addItemToCart(page, itemName);
  }
}

export async function openCart(page: Page) {
  await page.locator('[data-test="shopping-cart-link"]').click();
  await expect(page).toHaveURL(/cart\.html$/);
}

export async function startCheckout(page: Page) {
  await page.locator('[data-test="checkout"]').click();
  await expect(page).toHaveURL(/checkout-step-one\.html$/);
}

export async function fillCheckoutForm(
  page: Page,
  data: { firstName?: string; lastName?: string; postalCode?: string }
) {
  if (data.firstName !== undefined) {
    await page.locator('[data-test="firstName"]').fill(data.firstName);
  }
  if (data.lastName !== undefined) {
    await page.locator('[data-test="lastName"]').fill(data.lastName);
  }
  if (data.postalCode !== undefined) {
    await page.locator('[data-test="postalCode"]').fill(data.postalCode);
  }
}

export async function continueCheckout(page: Page) {
  await page.locator('[data-test="continue"]').click();
}

export async function expectOverview(page: Page, itemCount: number) {
  await expect(page).toHaveURL(/checkout-step-two\.html$/);
  await expect(page.locator('.cart_item')).toHaveCount(itemCount);
  await expect(page.locator('[data-test="payment-info-value"]')).toHaveText('SauceCard #31337');
  await expect(page.locator('[data-test="shipping-info-value"]')).toHaveText('Free Pony Express Delivery!');
  await expect(page.locator('[data-test="finish"]')).toBeVisible();
}

export async function finishCheckout(page: Page) {
  await page.locator('[data-test="finish"]').click();
  await expect(page).toHaveURL(/checkout-complete\.html$/);
  await expect(page.locator('[data-test="complete-header"]')).toHaveText('Thank you for your order!');
}

export async function cartItemNames(page: Page) {
  return page.locator('.inventory_item_name').allInnerTexts();
}

export async function parseMoneyLabel(page: Page, selector: string) {
  const text = await page.locator(selector).innerText();
  const value = Number(text.replace(/[^0-9.]/g, ''));
  return { text, value };
}
