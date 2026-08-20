import { expect, test, type Page } from '@playwright/test';

import { discoverAdaptiveCheckoutProfile } from './discovery';
import { buildRandomUsAddress } from './random-data';
import { readStoryConfig, type CheckoutPreference } from './story';

async function dismissCookieBanner(page: Page) {
  for (const label of ['Decline', 'Accept', 'Close', 'Got it']) {
    const button = page.getByRole('button', { name: new RegExp(`^${label}$`, 'i') }).first();
    if (await button.isVisible().catch(() => false)) {
      await button.click().catch(() => {});
      break;
    }
  }
}

async function clickIfVisible(page: Page, selectors: string[]) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.isVisible().catch(() => false)) {
      await locator.click();
      return true;
    }
  }
  return false;
}

async function fillByLabel(page: Page, label: RegExp, value: string) {
  const field = page.getByLabel(label).first();
  if (await field.isVisible().catch(() => false)) {
    const inputType = await field.getAttribute('type');
    if (inputType === 'radio' || inputType === 'checkbox') {
      return false;
    }
    await field.fill(value);
    return true;
  }
  return false;
}

async function fillBySelector(page: Page, selectors: string[], value: string) {
  for (const selector of selectors) {
    const field = page.locator(selector).first();
    if (await field.isVisible().catch(() => false)) {
      const inputType = await field.getAttribute('type');
      if (inputType === 'radio' || inputType === 'checkbox') {
        continue;
      }
      await field.fill(value);
      return true;
    }
  }
  return false;
}

async function fillTextboxByRole(page: Page, name: RegExp, value: string) {
  const field = page.getByRole('textbox', { name }).first();
  if (await field.isVisible().catch(() => false)) {
    await field.fill(value);
    return true;
  }
  return false;
}

async function selectByLabel(page: Page, label: RegExp, value: string) {
  const field = page.getByLabel(label).first();
  if (await field.isVisible().catch(() => false)) {
    await field.selectOption({ label: value }).catch(async () => {
      await field.selectOption(value);
    });
    return true;
  }
  return false;
}

async function selectAnyState(page: Page, valueHint: string) {
  for (const label of [/State/i, /Province/i]) {
    const field = page.getByLabel(label).first();
    if (await field.isVisible().catch(() => false)) {
      const options = await field.locator('option').allTextContents();
      const cleaned = options.map((option) => option.trim()).filter(Boolean);
      const preferred =
        cleaned.find((option) => option === valueHint || option.includes(valueHint)) ??
        cleaned.find((option) => option.length >= 2 && !/select/i.test(option));
      if (preferred) {
        await field.selectOption({ label: preferred }).catch(async () => {
          await field.selectOption(preferred);
        });
        return true;
      }
    }
  }
  return false;
}

async function selectAnyShippingMethod(page: Page) {
  const shippingRadio = page
    .locator('input[type="radio"]')
    .filter({ has: page.locator('xpath=following-sibling::*') })
    .first();

  const shippingLabels = page.locator('label').filter({ hasText: /mail|ground|ups|usps|shipping/i });
  const count = await shippingLabels.count();
  for (let index = 0; index < count; index += 1) {
    const label = shippingLabels.nth(index);
    if (await label.isVisible().catch(() => false)) {
      await label.click().catch(() => {});
      return true;
    }
  }

  if (await shippingRadio.isVisible().catch(() => false)) {
    await shippingRadio.check().catch(async () => {
      await shippingRadio.click();
    });
    return true;
  }

  return false;
}

async function selectRequestedShippingMethod(page: Page, shippingMethod: string) {
  if (/^any$/i.test(shippingMethod.trim())) {
    return selectAnyShippingMethod(page);
  }

  const radio = page.getByRole('radio', { name: new RegExp(shippingMethod, 'i') }).first();
  if (await radio.isVisible().catch(() => false)) {
    await radio.check().catch(async () => {
      await radio.click();
    });
    return true;
  }

  const label = page.locator('label').filter({ hasText: new RegExp(shippingMethod, 'i') }).first();
  if (await label.isVisible().catch(() => false)) {
    await label.click().catch(() => {});
    return true;
  }

  return false;
}

async function selectPaymentMethod(
  page: Page,
  preference: CheckoutPreference,
  randomHouseAccount: string
) {
  const paymentMethod = preference.paymentMethod.trim();
  const paymentRadio = page.getByRole('radio', { name: new RegExp(paymentMethod, 'i') }).first();

  if (await paymentRadio.isVisible().catch(() => false)) {
    await paymentRadio.check().catch(async () => {
      await paymentRadio.click();
    });
  } else {
    const selected = await clickIfVisible(page, [
      `label:has-text("${paymentMethod}")`,
      `text=${paymentMethod}`,
      'input[type="radio"][value*="house" i]',
      'input[type="radio"][value*="credit" i]',
      'input[type="radio"][value*="paypal" i]',
      'input[type="radio"][value*="purchase" i]',
    ]);

    if (!selected) {
      return false;
    }
  }

  await page.waitForTimeout(1000);

  if (/house account/i.test(paymentMethod)) {
    const detailValue =
      /^random$/i.test(preference.paymentDetail.trim()) || preference.paymentDetail.trim() === ''
        ? randomHouseAccount
        : preference.paymentDetail.trim();

    const filled = await fillByLabel(page, /House Account Number/i, detailValue);
    if (filled) {
      return true;
    }

    const filledByRole = await fillTextboxByRole(page, /House Account Number/i, detailValue);
    if (filledByRole) {
      return true;
    }

    return fillBySelector(
      page,
      [
        'input[name*="house" i]:not([type="radio"]):not([type="checkbox"])',
        'input[id*="house" i]:not([type="radio"]):not([type="checkbox"])',
        'input[name*="account" i]:not([type="radio"]):not([type="checkbox"])',
        'input[id*="account" i]:not([type="radio"]):not([type="checkbox"])',
      ],
      detailValue
    );
  }

  if (/purchase order/i.test(paymentMethod)) {
    const detailValue =
      /^random$/i.test(preference.paymentDetail.trim()) || preference.paymentDetail.trim() === ''
        ? `PO-${Date.now()}`
        : preference.paymentDetail.trim();

    const filled = await fillByLabel(page, /Purchase Order/i, detailValue);
    if (filled) {
      return true;
    }

    return fillBySelector(
      page,
      [
        'input[name*="purchase" i]:not([type="radio"])',
        'input[id*="purchase" i]:not([type="radio"])',
        'input[name*="order" i]:not([type="radio"])',
        'input[id*="order" i]:not([type="radio"])',
      ],
      detailValue
    );
  }

  return true;
}

async function continueToReview(page: Page) {
  return clickIfVisible(page, [
    'button:has-text("Continue to review")',
    'input[value*="Continue to review" i]',
    'button:has-text("Review")',
    'input[value*="Review" i]',
    'button:has-text("Continue")',
    'input[value*="Continue" i]',
  ]);
}

async function completePurchase(page: Page) {
  return clickIfVisible(page, [
    'button:has-text("Complete purchase")',
    'input[value*="Complete purchase" i]',
    'button:has-text("Place order")',
    'input[value*="Place order" i]',
    'button:has-text("Submit order")',
    'input[value*="Submit order" i]',
    'button:has-text("Complete")',
    'input[value*="Complete" i]',
  ]);
}

test.describe.serial('Pantheon guided checkout', () => {
  test.setTimeout(180000);
  const story = readStoryConfig();

  for (const preference of story.checkoutPreferences) {
    test(`completes Pantheon checkout for preference: ${preference.name}`, async ({ browser }) => {
    expect(story.baseUrl).toContain('pantheonsite.io');

    const profile = await discoverAdaptiveCheckoutProfile(browser, story);
    const random = buildRandomUsAddress();
    const context = await browser.newContext();
    const page = await context.newPage();

    try {
      await page.goto(profile.login.url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await dismissCookieBanner(page);
      await page.locator(profile.login.usernameSelector!).fill(story.credentials.username);
      await page.locator(profile.login.passwordSelector!).fill(story.credentials.password);
      await page.locator(profile.login.submitSelector!).click();
      await page.waitForLoadState('domcontentloaded');

      if (profile.home.productHref?.includes('/books')) {
        await page.goto(profile.home.productHref, { waitUntil: 'domcontentloaded', timeout: 60000 });
      } else {
        const openedBooks = await clickIfVisible(page, [
          'a[href*="/books"]',
          'text=Books',
          'a[href*="/product/"]',
        ]);
        if (openedBooks) {
          await page.waitForLoadState('domcontentloaded');
        }
      }

      await page.goto(profile.product.url!, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await dismissCookieBanner(page);
      await page.locator(profile.product.addToCartSelector!).click();
      await page.waitForTimeout(1500);

      if (profile.home.cartSelector && (await page.locator(profile.home.cartSelector).first().isVisible().catch(() => false))) {
        await page.locator(profile.home.cartSelector).first().click();
      } else {
        await page.goto(profile.cart.url ?? new URL('/cart', story.baseUrl).toString(), {
          waitUntil: 'domcontentloaded',
          timeout: 60000,
        });
      }

      await page.waitForLoadState('domcontentloaded');
      await clickIfVisible(page, ['button.checkout', profile.cart.checkoutSelector!].filter(Boolean));
      await page.waitForLoadState('domcontentloaded');
      await page.waitForTimeout(1000);

      await fillByLabel(page, /Email address/i, random.email);
      await fillByLabel(page, /First name/i, random.firstName);
      await fillByLabel(page, /Last name/i, random.lastName);
      await fillByLabel(page, /Company/i, random.company);
      await fillByLabel(page, /Street address$/i, random.street1);
      await fillByLabel(page, /Street address line 2/i, random.street2);
      await fillByLabel(page, /City/i, random.city);
      await fillByLabel(page, /Zip code|Postal code/i, random.postalCode);
      await fillByLabel(page, /Phone/i, random.phone);
      await selectAnyState(page, random.state);

      const selectedShipping = await selectRequestedShippingMethod(page, preference.shippingMethod);
      expect(selectedShipping).toBeTruthy();

      const selectedPayment = await selectPaymentMethod(
        page,
        preference,
        random.houseAccountNumber
      );
      expect(selectedPayment).toBeTruthy();

      if (preference.reviewBeforePurchase || preference.stopAfter === 'review' || preference.stopAfter === 'purchase') {
        const movedToReview = await continueToReview(page);
        expect(movedToReview).toBeTruthy();
        await page.waitForLoadState('domcontentloaded');
        await page.waitForTimeout(1500);
      }

      if (preference.completePurchase && preference.stopAfter === 'purchase') {
        const completed = await completePurchase(page);
        expect(completed).toBeTruthy();
        await page.waitForLoadState('domcontentloaded');
      }

      await test.info().attach('final-url', {
        body: page.url(),
        contentType: 'text/plain',
      });
    } finally {
      await context.close();
    }
    });
  }
});
