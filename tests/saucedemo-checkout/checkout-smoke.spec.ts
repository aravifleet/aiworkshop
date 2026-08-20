import { expect, test } from '@playwright/test';

import { CHECKOUT_DATA, ITEMS } from './test-data';
import {
  addItemsToCart,
  cartItemNames,
  continueCheckout,
  expectOverview,
  fillCheckoutForm,
  finishCheckout,
  openCart,
  parseMoneyLabel,
  startCheckout,
} from './helpers/checkout';
import { login } from './helpers/session';

test.describe('SCRUM-101 checkout smoke', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
  });

  test('HP01 completes checkout with one item', async ({ page }) => {
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);

    await expect(page.locator('.inventory_item_name')).toHaveText([ITEMS.backpack]);
    await expect(page.locator('.cart_quantity')).toHaveText(['1']);
    await expect(page.getByRole('button', { name: 'Continue Shopping' })).toBeVisible();
    await expect(page.getByRole('button', { name: 'Checkout' })).toBeVisible();

    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.valid);
    await continueCheckout(page);
    await expectOverview(page, 1);
    await finishCheckout(page);

    await expect(page.getByRole('button', { name: 'Back Home' })).toBeVisible();
  });

  test('HP02 completes checkout with two items and verifies totals', async ({ page }) => {
    await addItemsToCart(page, [ITEMS.backpack, ITEMS.bikeLight]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.alternate);
    await continueCheckout(page);
    await expectOverview(page, 2);

    const itemNames = await cartItemNames(page);
    expect(itemNames).toEqual([ITEMS.backpack, ITEMS.bikeLight]);

    const prices = await page.locator('.inventory_item_price').allInnerTexts();
    const numericPrices = prices.map((price) => Number(price.replace('$', '')));
    const subtotal = await parseMoneyLabel(page, '[data-test="subtotal-label"]');
    const tax = await parseMoneyLabel(page, '[data-test="tax-label"]');
    const total = await parseMoneyLabel(page, '[data-test="total-label"]');
    const expectedSubtotal = Number(
      numericPrices.reduce((sum, price) => sum + price, 0).toFixed(2)
    );

    expect(subtotal.value).toBe(expectedSubtotal);
    expect(Number((subtotal.value + tax.value).toFixed(2))).toBe(total.value);
  });

  test('HP03 continues shopping from cart without losing cart state', async ({ page }) => {
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await page.getByRole('button', { name: 'Continue Shopping' }).click();
    await expect(page).toHaveURL(/inventory\.html$/);
    await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1');
  });

  test('HP04 returns to products after order completion', async ({ page }) => {
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.valid);
    await continueCheckout(page);
    await finishCheckout(page);

    await page.getByRole('button', { name: 'Back Home' }).click();
    await expect(page).toHaveURL(/inventory\.html$/);
  });
});
