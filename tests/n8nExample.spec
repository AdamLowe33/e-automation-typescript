Here is a complete, self-contained Playwright test file in TypeScript that navigates to Google, handles a potential consent banner, searches for "Tres Leches Cake", and asserts on the results.

File: tests/google-search.spec.ts

```ts
import { test, expect, Page } from '@playwright/test';

async function acceptGoogleConsent(page: Page) {
  // Common consent button texts across locales
  const selectors = [
    'button:has-text("I agree")',
    'button:has-text("I Accept")',
    'button:has-text("I accept all")',
    'button:has-text("Aceptar")',
    'button:has-text("Acepto")',
    'button:has-text("Agree")',
  ];

  // Try to click any matching button on the main page
  for (const sel of selectors) {
    const btn = page.locator(sel);
    if (await btn.count() > 0) {
      await btn.first().click();
      await page.waitForTimeout(500);
      return;
    }
  }

  // If the consent is inside a frame, try there as well
  for (const frame of page.frames()) {
    for (const sel of selectors) {
      const btn = frame.locator(sel);
      if (await btn.count() > 0) {
        await btn.first().click();
        await page.waitForTimeout(500);
        return;
      }
    }
  }
}

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  await page.goto('https://www.google.com');

  // Attempt to dismiss cookie/consent dialog if present
  await acceptGoogleConsent(page);

  // Locate the search input and perform a search
  const searchBox = page.locator('input[name="q"]');
  await searchBox.waitFor({ state: 'visible', timeout: 10000 });

  await searchBox.fill('Tres Leches Cake');
  await searchBox.press('Enter');

  // Wait for the search results container to appear
  const results = page.locator('#search');
  await results.waitFor({ state: 'visible', timeout: 15000 });

  // Basic assertions
  await expect(page).toHaveTitle(/Tres Leches Cake/i);
  await expect(results).toBeVisible();
});
```

Notes:
- The test handles common consent/cookie banners by clicking a button with typical texts (I agree, I Accept, Aceptar, etc.). If your locale uses different text, you can extend the selectors array.
- The test asserts that the page title contains "Tres Leches Cake" and that the results container is visible.
- To run: ensure you have Playwright installed, then run npx playwright test.