import { expect, test } from '@playwright/test';

import { ITEMS } from './test-data';
import {
  addItemsToCart,
  continueCheckout,
  fillCheckoutForm,
  openCart,
  startCheckout,
} from './helpers/checkout';
import { login } from './helpers/session';

test.describe('SCRUM-101 checkout validation', () => {
  test.beforeEach(async ({ page }) => {
    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
  });

  test('NG01 blocks empty first name', async ({ page }) => {
    await fillCheckoutForm(page, { firstName: '', lastName: 'Doe', postalCode: '12345' });
    await continueCheckout(page);
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
    await expect(page.locator('[data-test="error"]')).toHaveText('Error: First Name is required');
  });

  test('NG02 blocks empty last name', async ({ page }) => {
    await fillCheckoutForm(page, { firstName: 'John', lastName: '', postalCode: '12345' });
    await continueCheckout(page);
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
    await expect(page.locator('[data-test="error"]')).toHaveText('Error: Last Name is required');
  });

  test('NG03 blocks empty postal code', async ({ page }) => {
    await fillCheckoutForm(page, { firstName: 'John', lastName: 'Doe', postalCode: '' });
    await continueCheckout(page);
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
    await expect(page.locator('[data-test="error"]')).toHaveText('Error: Postal Code is required');
  });

  test('NG04 blocks submitting the form with all fields empty', async ({ page }) => {
    await fillCheckoutForm(page, { firstName: '', lastName: '', postalCode: '' });
    await continueCheckout(page);
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
    await expect(page.locator('[data-test="error"]')).toHaveText('Error: First Name is required');
  });

  test('EC02 cancel from checkout info returns to cart', async ({ page }) => {
    await page.locator('[data-test="cancel"]').click();
    await expect(page).toHaveURL(/cart\.html$/);
    await expect(page.locator('.inventory_item_name')).toHaveText([ITEMS.backpack]);
  });
});
