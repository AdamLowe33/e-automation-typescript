// google-search.spec.ts
import { test, expect } from '@playwright/test';

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  // Go to Google
  await page.goto('https://www.google.com');

  // Handle cookie consent if present (locales vary)
  const consentSelectors = [
    'button:has-text("I agree")',
    'button:has-text("Agree")',
    'button:has-text("Aceptar")',
    'button:has-text("Accept all")',
  ];
  for (const selector of consentSelectors) {
    const btn = page.locator(selector);
    if (await btn.count() > 0) {
      await btn.first().click();
      break;
    }
  }

  // Type query and submit
  await page.fill('input[name="q"]', 'Tres Leches Cake');
  await page.keyboard.press('Enter');

  // Wait for results to render
  const searchRoot = page.locator('#search');
  await expect(searchRoot).toBeVisible({ timeout: 10000 });

  // Optional: verify there is at least one result
  const firstResult = searchRoot.locator('h3').first();
  await expect(firstResult).toBeVisible({ timeout: 10000 });
});