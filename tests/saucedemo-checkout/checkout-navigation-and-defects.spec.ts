import { expect, test } from '@playwright/test';

import { BASE_URL, CHECKOUT_DATA, ITEMS } from './test-data';
import {
  addItemsToCart,
  continueCheckout,
  expectOverview,
  fillCheckoutForm,
  finishCheckout,
  openCart,
  startCheckout,
} from './helpers/checkout';
import { gotoLogin, login } from './helpers/session';

test.describe('SCRUM-101 navigation, state, and known gaps', () => {
  test('EC03 cancel from overview returns to inventory', async ({ page }) => {
    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.valid);
    await continueCheckout(page);
    await expectOverview(page, 1);

    await page.locator('[data-test="cancel"]').click();
    await expect(page).toHaveURL(/inventory\.html$/);
    await expect(page.locator('[data-test="shopping-cart-badge"]')).toHaveText('1');
  });

  test('EC04 successful order clears the cart', async ({ page }) => {
    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.valid);
    await continueCheckout(page);
    await finishCheckout(page);

    await page.getByRole('button', { name: 'Back Home' }).click();
    await openCart(page);
    await expect(page.locator('.cart_item')).toHaveCount(0);
  });

  test('EC05 browser back from overview returns to checkout information', async ({ page }) => {
    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.valid);
    await continueCheckout(page);
    await expectOverview(page, 1);

    await page.goBack();
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
  });

  test('UI mobile checkout info controls remain visible', async ({ browser }) => {
    const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
    const page = await context.newPage();
    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);

    await expect(page.locator('[data-test="firstName"]')).toBeVisible();
    await expect(page.locator('[data-test="lastName"]')).toBeVisible();
    await expect(page.locator('[data-test="postalCode"]')).toBeVisible();
    await expect(page.locator('[data-test="continue"]')).toBeVisible();
    await expect(page.locator('[data-test="cancel"]')).toBeVisible();

    await context.close();
  });

  test('BUG-SCRUM101-01 invalid checkout data should be blocked', async ({ page }) => {
    test.fail(true, 'Known defect: invalid name and postal code formats are accepted.');

    await login(page);
    await addItemsToCart(page, [ITEMS.backpack]);
    await openCart(page);
    await startCheckout(page);
    await fillCheckoutForm(page, CHECKOUT_DATA.invalidFirstName);
    await continueCheckout(page);
    await expect(page).toHaveURL(/checkout-step-one\.html$/);
    await expect(page.locator('[data-test="error"]')).toBeVisible();
  });

  test('BUG-SCRUM101-02 empty cart should not enter checkout', async ({ page }) => {
    test.fail(true, 'Known defect: empty cart can still proceed to checkout.');

    await login(page);
    await openCart(page);
    await page.locator('[data-test="checkout"]').click();
    await expect(page).toHaveURL(/cart\.html$/);
  });

  test('EC06 logged-out users are redirected away from cart and checkout step one', async ({ page }) => {
    await gotoLogin(page);
    await page.goto(`${BASE_URL}/cart.html`, { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveURL(/saucedemo\.com\/?$/);

    await page.goto(`${BASE_URL}/checkout-step-one.html`, { waitUntil: 'domcontentloaded' });
    await expect(page).toHaveURL(/saucedemo\.com\/?$/);
  });
});
