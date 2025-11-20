```ts
// tests/google-search.spec.ts

import { test, expect } from '@playwright/test';
import type { Page } from '@playwright/test';

/**
 * Try to close common Google cookie/privacy consent banners.
 * This is intentionally simple to keep the test robust across regions.
 */
async function acceptGoogleConsent(page: Page) {
  const selectors = [
    'button:has-text("I agree")',
    'button:has-text("I Agree")',
    'button:has-text("Accept all")',
    'button:has-text("Accept cookies")',
    'button:has-text("Got it")',
    'button:has-text("Okay")',
    'button:has-text("Akzeptieren")',
  ];

  for (const sel of selectors) {
    const btn = page.locator(sel);
    if ((await btn.count()) > 0 && (await btn.first().isVisible())) {
      await btn.first().click();
      // Give a moment for the banner to disappear
      await page.waitForTimeout(500);
      break;
    }
  }
}

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded' });

  // Try to close consent banners if they appear
  await acceptGoogleConsent(page);

  // Locate Google search box and perform a search
  const searchBox = page.locator('input[name="q"]');
  await searchBox.waitFor({ state: 'visible' });
  await searchBox.fill('Tres Leches Cake');
  await page.keyboard.press('Enter');

  // Basic verifications: URL contains search and results container is visible
  await expect(page).toHaveURL(/.*search.*/);
  const results = page.locator('#search');
  await expect(results).toBeVisible();
});
```