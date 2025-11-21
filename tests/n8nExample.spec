Here is a complete working TypeScript Playwright test file that navigates to Google and searches for "Tres Leches Cake".

Save as: tests/google-search.spec.ts

```ts
import { test, expect } from '@playwright/test';

test('Google search for Tres Leches Cake', async ({ page }) => {
  // Navigate to Google
  await page.goto('https://www.google.com/');

  // Handle common consent banners (if present)
  const consentSelectors = [
    'button:has-text("I agree")',
    'button:has-text("Agree")',
    'button:has-text("Accept all")',
    'button:has-text("Aceptar")',
    'button:has-text("I consent")',
  ];

  for (const sel of consentSelectors) {
    const el = page.locator(sel);
    if (await el.count() > 0) {
      await el.first().click();
      break;
    }
  }

  // Perform search
  const searchBox = page.locator('input[name="q"]');
  await searchBox.fill('Tres Leches Cake');

  // Press Enter and wait for navigation to search results
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'load' }),
    searchBox.press('Enter')
  ]);

  // Basic assertions
  // URL should indicate a Google search results page
  await expect(page).toHaveURL(/\/search\?/);
  // Title should reflect the query (case-insensitive)
  await expect(page).toHaveTitle(/Tres Leches Cake/i);
  // Ensure results container is visible
  const results = page.locator('#search');
  await expect(results).toBeVisible();
});
```