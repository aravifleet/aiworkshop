import { existsSync, readdirSync, readFileSync } from 'node:fs';
import path from 'node:path';

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

function readUserStory() {
  const storyPath = resolveUserStoryPath();
  const storyText = readFileSync(storyPath, 'utf8');
  return { storyPath, storyText };
}

function extractRequiredMatch(storyText: string, regex: RegExp, label: string) {
  const match = storyText.match(regex);
  if (!match?.[1]) {
    throw new Error(`Unable to extract ${label} from the user story.`);
  }
  return match[1].trim();
}

const { storyPath, storyText } = readUserStory();

export const ACTIVE_USER_STORY_PATH = storyPath;

export const BASE_URL = extractRequiredMatch(
  storyText,
  /## Application URL\s+([^\r\n]+)/i,
  'application URL'
);

export const USERS = {
  standard: {
    username: extractRequiredMatch(
      storyText,
      /-\s+Username:\s+`?([^\r\n`]+)`?/i,
      'username'
    ),
    password: extractRequiredMatch(
      storyText,
      /-\s+Password:\s+`?([^\r\n`]+)`?/i,
      'password'
    ),
  },
};

export const ITEMS = {
  backpack: 'Sauce Labs Backpack',
  bikeLight: 'Sauce Labs Bike Light',
};

export const CHECKOUT_DATA = {
  valid: {
    firstName: 'John',
    lastName: 'Doe',
    postalCode: '12345',
  },
  alternate: {
    firstName: 'Jane',
    lastName: 'Smith',
    postalCode: '560001',
  },
  invalidFirstName: {
    firstName: '@#!',
    lastName: 'Doe',
    postalCode: '12345',
  },
  invalidLastName: {
    firstName: 'John',
    lastName: '1234',
    postalCode: '12345',
  },
  invalidPostalCodeShort: {
    firstName: 'John',
    lastName: 'Doe',
    postalCode: '12',
  },
  invalidPostalCodeAlpha: {
    firstName: 'John',
    lastName: 'Doe',
    postalCode: 'ABCDE',
  },
};
