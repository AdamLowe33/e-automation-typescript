Sure. Here’s a ready-to-use Playwright test in TypeScript that navigates to Google and searches for "Tres Leches Cake". It includes handling a possible consent banner and a basic assertion that the results page loads.

Files you can create:

1) tests/google-search.spec.ts
- This is a self-contained test file written in TypeScript.

Code:
import { test, expect } from '@playwright/test';

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  // Go to Google
  await page.goto('https://www.google.com');

  // Optional: handle consent banner if it appears
  // Try common button texts across locales
  const consentSelectors = [
    'button:has-text("I agree")',
    'button:has-text("I Accept")',
    'button:has-text("Accept all")'
  ];
  for (const selector of consentSelectors) {
    const btn = page.locator(selector);
    if (await btn.count() > 0) {
      await btn.first().click();
      break;
    }
  }

  // Find the search box, type query, and submit
  const searchBox = page.locator('input[name="q"]');
  await searchBox.waitFor({ state: 'visible', timeout: 5000 });
  await searchBox.fill('Tres Leches Cake');
  await searchBox.press('Enter');

  // Wait for results to load
  await page.waitForSelector('#search', { timeout: 10000 });

  // Basic assertions
  await expect(page).toHaveURL(/q=.*Tres.*Leches.*Cake|q=.*Tres%20Leches%20Cake/i);
  const firstResultLink = page.locator('#search a').first();
  await expect(firstResultLink).toBeVisible();
});

2) Optional: playwright.config.ts (config for TypeScript projects)
Code:
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 30 * 1000,
  retries: 0,
  use: {
    headless: true,
    // You can set a baseURL if you prefer
    // baseURL: 'https://www.google.com',
  },
});

3) Optional: tsconfig.json (TypeScript config)
Code:
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "strict": true,
    "jsx": "react",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true
  },
  "include": ["**/*.ts"]
}

4) package.json (dependencies and scripts)
Code:
{
  "name": "playwright-google-search",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "test": "playwright test"
  },
  "devDependencies": {
    "@playwright/test": "^1.40.0"
  }
}

How to run
- Install Playwright and dependencies:
  - npm init -y
  - npm i -D @playwright/test
  - npx playwright install
- Run tests:
  - npm test

Notes
- Google sometimes shows consent banners or blocks automation. The test includes a small step to click common consent buttons if they appear. If Google changes its UI or your locale differs, you may need to adjust the selectors accordingly.
- The test uses a basic assertion that the results container (#search) is present and that the URL includes a query for Tres Leches Cake. You can expand assertions to check specific result content if needed.