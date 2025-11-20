// File: tests/google-search.spec.ts
import { test, expect, Page } from '@playwright/test';

async function acceptConsent(page: Page): Promise<void> {
  // Common selectors for Google consent banners
  const selectors = [
    '#L2AGLb', // typical Google consent button
    'button:has-text("I agree")',
    'button:has-text("Accept all")',
    'text=I agree',
    'text=Accept all',
  ];

  // Try the main page first
  for (const sel of selectors) {
    const btn = page.locator(sel);
    if (await btn.count() > 0) {
      await btn.first().click({ timeout: 3000 }).catch(() => {});
      return;
    }
  }

  // If not found on main page, try within iframes
  for (const frame of page.frames()) {
    for (const sel of selectors) {
      const btn = frame.locator(sel);
      if (await btn.count() > 0) {
        await btn.first().click({ timeout: 3000 }).catch(() => {});
        return;
      }
    }
  }
}

test('Google search for Tres Leches Cake', async ({ page }) => {
  await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded' });

  // Attempt to dismiss consent if present
  await acceptConsent(page);

  // Perform search
  const searchBox = page.locator('input[name="q"]');
  await searchBox.waitFor({ state: 'visible', timeout: 10000 });
  await searchBox.fill('Tres Leches Cake');
  await searchBox.press('Enter');

  // Wait for results page
  await page.waitForURL(/.*google.*search.*/);

  // Basic assertions to verify navigation and content
  await expect(page).toHaveTitle(/Tres Leches Cake|Google/);
  const results = page.locator('#search');
  await expect(results).toBeVisible();
});