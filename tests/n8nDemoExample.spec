// File: google-search.spec.ts
import { test, expect } from '@playwright/test';
import type { Page } from '@playwright/test';

// Helper to dismiss common Google cookie consent prompts if they appear
async function acceptGoogleCookies(page: Page) {
  const selectors = [
    'button:has-text("I agree")',
    'button:has-text("I Accept")',
    'button:has-text("Accept all")',
    'button:has-text("Agree")',
    'button:has-text("Accept")',
    '#L2AGLb', // common Google consent id
  ];

  for (const selector of selectors) {
    const el = page.locator(selector);
    const count = await el.count();
    if (count > 0) {
      await el.first().click();
      await page.waitForTimeout(500); // small pause to allow dialog to close
      break;
    }
  }
}

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  // Navigate to Google
  await page.goto('https://www.google.com');

  // Attempt to dismiss cookie consent if it appears
  await acceptGoogleCookies(page);

  // Type into the search box and submit
  const searchInput = page.locator('input[name="q"]');
  await searchInput.waitFor({ state: 'visible', timeout: 10000 });
  await searchInput.fill('Tres Leches Cake');

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle' }),
    searchInput.press('Enter')
  ]);

  // Wait for the results container to ensure the page loaded
  await page.waitForSelector('#search', { timeout: 10000 });

  // Basic assertion: URL should reflect the search query
  await expect(page).toHaveURL(/q=(?:Tres%20Leches%20Cake|Tres\+Leches\+Cake|Tres Leches Cake)/);
});