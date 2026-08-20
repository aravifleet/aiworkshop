import { mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';

import type { Browser, Locator, Page } from '@playwright/test';

import type { StoryConfig } from './story';

export type AppProfile = {
  artifacts: {
    gapReportPath: string;
    profilePath: string;
  };
  capabilities: {
    addToCart: boolean;
    cartAccess: boolean;
    checkoutEntry: boolean;
    checkoutForm: boolean;
    login: boolean;
  };
  cart: {
    checkoutSelector: string | null;
    itemCountEstimate: number;
    removeButtonCount: number;
    url: string | null;
  };
  checkout: {
    discoveredFieldLabels: string[];
    firstNameSelector: string | null;
    lastNameSelector: string | null;
    postalCodeSelector: string | null;
    url: string | null;
  };
  gaps: string[];
  generatedAt: string;
  home: {
    cartHref: string | null;
    cartSelector: string | null;
    loginHref: string | null;
    productHref: string | null;
    title: string;
    url: string;
  };
  login: {
    logoutDetected: boolean;
    passwordSelector: string | null;
    submitSelector: string | null;
    success: boolean;
    successUrl: string | null;
    url: string;
    usernameSelector: string | null;
  };
  product: {
    addToCartSelector: string | null;
    quantitySelector: string | null;
    title: string | null;
    url: string | null;
  };
  story: {
    baseUrl: string;
    path: string;
    title: string;
  };
};

type CandidateAnchor = {
  href: string;
  text: string;
};

function uniqueStrings(values: string[]) {
  return [...new Set(values.map((value) => value.trim()).filter(Boolean))];
}

async function dismissCookieBanner(page: Page) {
  for (const label of ['Decline', 'Accept', 'Close', 'Got it']) {
    const button = page.getByRole('button', { name: new RegExp(`^${label}$`, 'i') }).first();
    if (await button.isVisible().catch(() => false)) {
      await button.click().catch(() => {});
      break;
    }
  }
}

async function firstVisibleSelector(page: Page, selectors: string[]) {
  for (const selector of selectors) {
    const locator = page.locator(selector).first();
    if (await locator.isVisible().catch(() => false)) {
      return selector;
    }
  }
  return null;
}

async function getCandidateAnchors(page: Page) {
  return page.locator('a[href]').evaluateAll((elements) =>
    elements.map((element) => ({
      href: element.getAttribute('href') ?? '',
      text: (element.textContent ?? '').replace(/\s+/g, ' ').trim(),
    }))
  ) as Promise<CandidateAnchor[]>;
}

function selectAnchorHref(anchors: CandidateAnchor[], patterns: RegExp[]) {
  const match = anchors.find((anchor) =>
    patterns.some((pattern) => pattern.test(`${anchor.text} ${anchor.href}`))
  );
  return match?.href ?? null;
}

function selectAnchorHrefs(anchors: CandidateAnchor[], patterns: RegExp[]) {
  return uniqueStrings(
    anchors
      .filter((anchor) => patterns.some((pattern) => pattern.test(`${anchor.text} ${anchor.href}`)))
      .map((anchor) => anchor.href)
  );
}

function resolveUrl(baseUrl: string, href: string | null) {
  if (!href) {
    return null;
  }
  return new URL(href, baseUrl).toString();
}

async function tryClick(locator: Locator) {
  if (await locator.isVisible().catch(() => false)) {
    await locator.click().catch(() => {});
    return true;
  }
  return false;
}

async function findCheckoutFieldSelector(page: Page, selectors: string[]) {
  return firstVisibleSelector(page, selectors);
}

async function findWorkingProductPage(
  page: Page,
  baseUrl: string,
  candidates: string[]
): Promise<{
  addToCartSelector: string | null;
  quantitySelector: string | null;
  title: string | null;
  url: string | null;
}> {
  const productCandidates = candidates
    .map((href) => resolveUrl(baseUrl, href))
    .filter((href): href is string => Boolean(href));

  for (const productUrl of productCandidates) {
    await page.goto(productUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await dismissCookieBanner(page);

    const addToCartSelector = await firstVisibleSelector(page, [
      '[data-test*="add-to-cart"]',
      'input[value="Add to cart"]:not([disabled])',
      'button:has-text("Add to cart"):not([disabled])',
      '[data-drupal-selector*="add-to-cart"] input[type="submit"]:not([disabled])',
      'input[type="submit"][value*="Add" i]:not([disabled])',
    ]);

    if (addToCartSelector) {
      const quantitySelector = await firstVisibleSelector(page, [
        '[data-test="item-quantity"]',
        'input[type="number"][name*="quantity" i]',
        'input[id*="quantity" i]',
      ]);

      return {
        addToCartSelector,
        quantitySelector,
        title: await page.title(),
        url: page.url(),
      };
    }
  }

  return {
    addToCartSelector: null,
    quantitySelector: null,
    title: null,
    url: null,
  };
}

function buildGapReport(profile: AppProfile) {
  const lines = [
    `# Adaptive Gap Report`,
    ``,
    `- Story: \`${profile.story.title}\``,
    `- Story file: \`${profile.story.path}\``,
    `- Base URL: \`${profile.story.baseUrl}\``,
    `- Generated: \`${profile.generatedAt}\``,
    ``,
    `## Discovered Capabilities`,
    `- Login: ${profile.capabilities.login ? 'Yes' : 'No'}`,
    `- Cart Access: ${profile.capabilities.cartAccess ? 'Yes' : 'No'}`,
    `- Add To Cart: ${profile.capabilities.addToCart ? 'Yes' : 'No'}`,
    `- Checkout Entry: ${profile.capabilities.checkoutEntry ? 'Yes' : 'No'}`,
    `- Checkout Form: ${profile.capabilities.checkoutForm ? 'Yes' : 'No'}`,
    ``,
    `## Key Routes`,
    `- Home: \`${profile.home.url}\``,
    `- Login: \`${profile.login.url}\``,
    `- Cart: \`${profile.cart.url ?? 'Not discovered'}\``,
    `- Product: \`${profile.product.url ?? 'Not discovered'}\``,
    `- Checkout: \`${profile.checkout.url ?? 'Not discovered'}\``,
    ``,
    `## Gaps`,
  ];

  if (profile.gaps.length === 0) {
    lines.push(`- No story-to-app gaps were detected during discovery.`);
  } else {
    for (const gap of profile.gaps) {
      lines.push(`- ${gap}`);
    }
  }

  return `${lines.join('\n')}\n`;
}

function saveArtifacts(story: StoryConfig, profile: AppProfile) {
  const artifactsDir = path.resolve(process.cwd(), 'artifacts');
  mkdirSync(artifactsDir, { recursive: true });

  const profilePath = path.join(artifactsDir, `${story.slug}-app-profile.json`);
  const gapReportPath = path.join(artifactsDir, `${story.slug}-gap-report.md`);

  profile.artifacts.profilePath = profilePath;
  profile.artifacts.gapReportPath = gapReportPath;

  writeFileSync(profilePath, JSON.stringify(profile, null, 2));
  writeFileSync(gapReportPath, buildGapReport(profile));
}

export async function discoverAdaptiveCheckoutProfile(browser: Browser, story: StoryConfig) {
  const context = await browser.newContext();
  const page = await context.newPage();

  const profile: AppProfile = {
    artifacts: {
      gapReportPath: '',
      profilePath: '',
    },
    capabilities: {
      addToCart: false,
      cartAccess: false,
      checkoutEntry: false,
      checkoutForm: false,
      login: false,
    },
    cart: {
      checkoutSelector: null,
      itemCountEstimate: 0,
      removeButtonCount: 0,
      url: null,
    },
    checkout: {
      discoveredFieldLabels: [],
      firstNameSelector: null,
      lastNameSelector: null,
      postalCodeSelector: null,
      url: null,
    },
    gaps: [],
    generatedAt: new Date().toISOString(),
    home: {
      cartHref: null,
      cartSelector: null,
      loginHref: null,
      productHref: null,
      title: '',
      url: story.baseUrl,
    },
    login: {
      logoutDetected: false,
      passwordSelector: null,
      submitSelector: null,
      success: false,
      successUrl: null,
      url: story.baseUrl,
      usernameSelector: null,
    },
    product: {
      addToCartSelector: null,
      quantitySelector: null,
      title: null,
      url: null,
    },
    story: {
      baseUrl: story.baseUrl,
      path: story.storyPath,
      title: story.title,
    },
  };

  try {
    await page.goto(story.baseUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await dismissCookieBanner(page);

    profile.home.title = await page.title();
    profile.home.url = page.url();

    const anchors = await getCandidateAnchors(page);
    const productCandidates = selectAnchorHrefs(anchors, [/\/book\//i, /\/product\//i]);
    const homeLoginSelector = await firstVisibleSelector(page, [
      '[data-test="username"]',
      'input[type="email"]',
      'input[name="username"]',
      'input[name="name"]',
    ]);
    const homePasswordSelector = await firstVisibleSelector(page, [
      '[data-test="password"]',
      'input[type="password"]',
    ]);
    const homeSubmitSelector = await firstVisibleSelector(page, [
      '[data-test="login-button"]',
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'input[type="submit"][value*="Log" i]',
      'input[type="submit"]',
      'button[type="submit"]',
    ]);
    profile.home.loginHref = resolveUrl(
      story.baseUrl,
      selectAnchorHref(anchors, [/log in/i, /sign in/i, /\/user\/login/i, /\/login/i])
    );
    profile.home.cartHref = resolveUrl(
      story.baseUrl,
      selectAnchorHref(anchors, [/\bcart\b/i, /\/cart/i, /cart\.html/i, /checkout/i])
    );
    profile.home.cartSelector = await firstVisibleSelector(page, [
      '[data-test="shopping-cart-link"]',
      'a[href*="cart.html"]',
      'a[href*="/cart"]',
      'text=Cart',
    ]);
    profile.home.productHref = resolveUrl(
      story.baseUrl,
      selectAnchorHref(anchors, [/\/book\//i, /\/product\//i])
    );

    const loginUrl =
      (homeLoginSelector && homePasswordSelector && homeSubmitSelector ? page.url() : null) ??
      profile.home.loginHref ??
      resolveUrl(story.baseUrl, '/user/login') ??
      resolveUrl(story.baseUrl, '/login') ??
      story.baseUrl;

    await page.goto(loginUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await dismissCookieBanner(page);

    profile.login.url = page.url();
    profile.login.usernameSelector = await firstVisibleSelector(page, [
      '[data-test="username"]',
      'input[type="email"]',
      'input[name="username"]',
      'input[name="email"]',
      'input[name="name"]',
      'input[id*="user" i]',
      'input[id*="email" i]',
    ]);
    profile.login.passwordSelector = await firstVisibleSelector(page, [
      '[data-test="password"]',
      'input[type="password"]',
      'input[name="password"]',
      'input[name="pass"]',
      'input[id*="pass" i]',
    ]);
    profile.login.submitSelector = await firstVisibleSelector(page, [
      '[data-test="login-button"]',
      'input[type="submit"][value*="Log" i]',
      'button:has-text("Log in")',
      'button:has-text("Login")',
      'input[type="submit"]',
      'button[type="submit"]',
    ]);

    if (
      profile.login.usernameSelector &&
      profile.login.passwordSelector &&
      profile.login.submitSelector
    ) {
      await page.locator(profile.login.usernameSelector).fill(story.credentials.username);
      await page.locator(profile.login.passwordSelector).fill(story.credentials.password);
      await page.locator(profile.login.submitSelector).click();
      await page.waitForLoadState('domcontentloaded');

      profile.login.successUrl = page.url();
      profile.login.logoutDetected = await page
        .locator('a[href*="logout"], text=Logout, #react-burger-menu-btn')
        .first()
        .isVisible()
        .catch(() => false);
      const passwordStillVisible = await page
        .locator(profile.login.passwordSelector)
        .first()
        .isVisible()
        .catch(() => false);

      profile.login.success = profile.login.logoutDetected || !passwordStillVisible;
      profile.capabilities.login = profile.login.success;

      const inventoryAddToCartSelector = await firstVisibleSelector(page, [
        '[data-test*="add-to-cart"]',
        'button:has-text("Add to cart")',
        'input[value="Add to cart"]',
      ]);
      if (!profile.home.productHref && inventoryAddToCartSelector) {
        profile.home.productHref = page.url();
      }
      if (!profile.home.cartSelector) {
        profile.home.cartSelector = await firstVisibleSelector(page, [
          '[data-test="shopping-cart-link"]',
          'a[href*="cart.html"]',
          'a[href*="/cart"]',
          'text=Cart',
        ]);
      }
    }

    if (productCandidates.length > 0) {
      const workingProduct = await findWorkingProductPage(page, story.baseUrl, productCandidates);
      profile.product.url = workingProduct.url;
      profile.product.title = workingProduct.title;
      profile.product.addToCartSelector = workingProduct.addToCartSelector;
      profile.product.quantitySelector = workingProduct.quantitySelector;
      profile.capabilities.addToCart = Boolean(profile.product.addToCartSelector);

      if (profile.product.url) {
        profile.home.productHref = profile.product.url;
      }

      if (profile.product.addToCartSelector) {
        await tryClick(page.locator(profile.product.addToCartSelector).first());
        await page.waitForTimeout(1500);
      }
    }

    if (profile.home.cartSelector && (await page.locator(profile.home.cartSelector).first().isVisible().catch(() => false))) {
      await page.locator(profile.home.cartSelector).first().click();
      await page.waitForLoadState('domcontentloaded');
    } else {
      const cartUrl =
        profile.home.cartHref ??
        resolveUrl(story.baseUrl, '/cart.html') ??
        resolveUrl(story.baseUrl, '/cart') ??
        `${story.baseUrl.replace(/\/$/, '')}/cart`;
      await page.goto(cartUrl, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await dismissCookieBanner(page);
    }

    profile.cart.url = page.url();
    const cartTitle = await page.title();
    profile.capabilities.cartAccess =
      /cart/i.test(page.url()) ||
      /shopping cart/i.test(cartTitle) ||
      (await page.locator('[data-test="checkout"], #edit-checkout, input[value="Checkout"]').count()) > 0;
    profile.cart.checkoutSelector = await firstVisibleSelector(page, [
      '[data-test="checkout"]',
      '#edit-checkout',
      'input[value="Checkout"]',
      'button:has-text("Checkout")',
      'a[href*="checkout"]',
    ]);
    profile.cart.removeButtonCount = await page
      .locator('input[id*="remove-button"], button:has-text("Remove"), input[value*="Remove" i]')
      .count();
    profile.cart.itemCountEstimate = profile.cart.removeButtonCount;
    profile.capabilities.checkoutEntry = Boolean(profile.cart.checkoutSelector);

    if (profile.cart.checkoutSelector) {
      const currentUrl = page.url();
      await tryClick(page.locator(profile.cart.checkoutSelector).first());
      await page.waitForTimeout(3000);

      const maybeNavigated = page.url();
      if (maybeNavigated !== currentUrl) {
        profile.checkout.url = maybeNavigated;
      }
    }

    if (profile.checkout.url && !/cart(?:\.html)?$/i.test(profile.checkout.url)) {
      profile.checkout.discoveredFieldLabels = uniqueStrings(
        (await page.locator('label').allInnerTexts()).slice(0, 50)
      );
      profile.checkout.firstNameSelector = await findCheckoutFieldSelector(page, [
        '[data-test="firstName"]',
        'input[name*="first" i]',
        'input[id*="first" i]',
      ]);
      profile.checkout.lastNameSelector = await findCheckoutFieldSelector(page, [
        '[data-test="lastName"]',
        'input[name*="last" i]',
        'input[id*="last" i]',
      ]);
      profile.checkout.postalCodeSelector = await findCheckoutFieldSelector(page, [
        '[data-test="postalCode"]',
        'input[name*="postal" i]',
        'input[id*="postal" i]',
        'input[name*="zip" i]',
        'input[id*="zip" i]',
      ]);
      profile.capabilities.checkoutForm = Boolean(
        profile.checkout.firstNameSelector ||
          profile.checkout.lastNameSelector ||
          profile.checkout.postalCodeSelector
      );
    }

    if (!profile.capabilities.login) {
      profile.gaps.push('Login flow could not be validated with the credentials from the user story.');
    }
    if (!profile.capabilities.addToCart) {
      profile.gaps.push('No add-to-cart control was discovered on a live product page.');
    }
    if (!profile.capabilities.checkoutEntry) {
      profile.gaps.push('No checkout entry point was discovered from the cart page.');
    }
    if (!profile.capabilities.checkoutForm) {
      profile.gaps.push(
        'A checkout information form with discoverable first name / last name / postal code fields was not reached.'
      );
    } else {
      if (!profile.checkout.firstNameSelector) {
        profile.gaps.push('The live checkout form does not expose a discoverable first-name field.');
      }
      if (!profile.checkout.lastNameSelector) {
        profile.gaps.push('The live checkout form does not expose a discoverable last-name field.');
      }
      if (!profile.checkout.postalCodeSelector) {
        profile.gaps.push('The live checkout form does not expose a discoverable postal/zip field.');
      }
    }
  } finally {
    saveArtifacts(story, profile);
    await context.close();
  }

  return profile;
}
