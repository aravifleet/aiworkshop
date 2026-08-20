import { existsSync, readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';

export type StoryConfig = {
  acceptanceCriteria: string[];
  baseUrl: string;
  checkoutPreferences: CheckoutPreference[];
  credentials: {
    password: string;
    username: string;
  };
  slug: string;
  storyPath: string;
  storyText: string;
  title: string;
};

export type CheckoutPreference = {
  addressStrategy: string;
  completePurchase: boolean;
  name: string;
  paymentDetail: string;
  paymentMethod: string;
  productSelection: string;
  reviewBeforePurchase: boolean;
  shippingMethod: string;
  stopAfter: 'purchase' | 'review';
};

function extractRequiredMatch(storyText: string, regex: RegExp, label: string) {
  const match = storyText.match(regex);
  if (!match?.[1]) {
    throw new Error(`Unable to extract ${label} from the user story.`);
  }
  return match[1].trim();
}

function resolveUserStoryPath() {
  const envStory = process.env.USER_STORY_FILE?.trim();
  if (envStory) {
    const envPath = path.resolve(process.cwd(), envStory);
    if (!existsSync(envPath)) {
      throw new Error(`USER_STORY_FILE does not exist: ${envPath}`);
    }
    return envPath;
  }

  const userStoriesDir = path.resolve(process.cwd(), 'user-stories');
  const markdownFiles = readdirSync(userStoriesDir)
    .filter((file) => file.toLowerCase().endsWith('.md'))
    .sort((left, right) => left.localeCompare(right));

  if (markdownFiles.length === 0) {
    throw new Error(`No markdown user stories found in: ${userStoriesDir}`);
  }

  if (markdownFiles.length > 1) {
    throw new Error(
      `Multiple user stories found in ${userStoriesDir}. Set USER_STORY_FILE to choose one: ${markdownFiles.join(', ')}`
    );
  }

  return path.join(userStoriesDir, markdownFiles[0]);
}

function extractAcceptanceCriteria(storyText: string) {
  return [...storyText.matchAll(/###\s+(AC\d+:\s+[^\r\n]+)/g)].map((match) => match[1].trim());
}

function extractPreferenceValue(block: string, label: string, fallback: string) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const match = block.match(new RegExp(`-\\s+${escaped}:\\s+([^\\r\\n]+)`, 'i'));
  return match?.[1]?.trim() ?? fallback;
}

function toBoolean(value: string, fallback: boolean) {
  if (/^(yes|true)$/i.test(value.trim())) {
    return true;
  }
  if (/^(no|false)$/i.test(value.trim())) {
    return false;
  }
  return fallback;
}

function extractCheckoutPreferences(storyText: string): CheckoutPreference[] {
  const matches = [
    ...storyText.matchAll(
      /###\s+Checkout Preference\s+(\d+)\s*[\r\n]+([\s\S]*?)(?=\n###\s+Checkout Preference\s+\d+|\n##\s+|$)/g
    ),
  ];

  if (matches.length === 0) {
    return [
      {
        addressStrategy: 'Random US address',
        completePurchase: true,
        name: 'Default checkout preference',
        paymentDetail: 'Random',
        paymentMethod: 'House Account',
        productSelection: 'First purchasable product',
        reviewBeforePurchase: true,
        shippingMethod: 'Any',
        stopAfter: 'purchase',
      },
    ];
  }

  return matches.map((match, index) => {
    const block = match[2];
    const stopAfter = extractPreferenceValue(block, 'Stop After', 'purchase').toLowerCase();

    return {
      addressStrategy: extractPreferenceValue(block, 'Address Strategy', 'Random US address'),
      completePurchase: toBoolean(extractPreferenceValue(block, 'Complete Purchase', 'Yes'), true),
      name: extractPreferenceValue(block, 'Name', `Checkout Preference ${index + 1}`),
      paymentDetail: extractPreferenceValue(block, 'Payment Detail', 'Random'),
      paymentMethod: extractPreferenceValue(block, 'Payment Method', 'House Account'),
      productSelection: extractPreferenceValue(
        block,
        'Product Selection',
        'First purchasable product'
      ),
      reviewBeforePurchase: toBoolean(
        extractPreferenceValue(block, 'Review Before Purchase', 'Yes'),
        true
      ),
      shippingMethod: extractPreferenceValue(block, 'Shipping Method', 'Any'),
      stopAfter: stopAfter === 'review' ? 'review' : 'purchase',
    };
  });
}

export function readStoryConfig(): StoryConfig {
  const storyPath = resolveUserStoryPath();
  const storyText = readFileSync(storyPath, 'utf8');
  const title =
    storyText.match(/^#\s+User Story:\s+([^\r\n]+)/m)?.[1]?.trim() ??
    path.basename(storyPath, path.extname(storyPath));

  return {
    acceptanceCriteria: extractAcceptanceCriteria(storyText),
    baseUrl: extractRequiredMatch(storyText, /## Application URL\s+([^\r\n]+)/i, 'application URL'),
    checkoutPreferences: extractCheckoutPreferences(storyText),
    credentials: {
      password: extractRequiredMatch(storyText, /-\s+Password:\s+`?([^\r\n`]+)`?/i, 'password'),
      username: extractRequiredMatch(storyText, /-\s+Username:\s+`?([^\r\n`]+)`?/i, 'username'),
    },
    slug: path.basename(storyPath, path.extname(storyPath)),
    storyPath,
    storyText,
    title,
  };
}
