```ts
// google-search.spec.ts
import { test, expect } from '@playwright/test';

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  // Go to Google homepage
  await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded' });

  // Handle cookie consent if it appears (text may vary by locale)
  const consentSelectors = [
    'button:has-text("I agree")',
    'button:has-text("Agree")',
    'button:has-text("Accept all")',
    'button:has-text("Accept")',
  ];
  for (const sel of consentSelectors) {
    const btn = page.locator(sel);
    if ((await btn.count()) > 0) {
      await btn.first().click();
      // Small pause to allow UI to update
      await page.waitForTimeout(500);
      break;
    }
  }

  // Find a search input using common selectors
  const searchInputs = [
    'input[name="q"]',
    'input[aria-label="Search"]',
    'input[title="Search"]',
  ];
  let searchBox: any = null;
  for (const sel of searchInputs) {
    const el = page.locator(sel);
    if ((await el.count()) > 0) {
      searchBox = el;
      break;
    }
  }

  // Perform the search
  if (searchBox) {
    await searchBox.first().fill('Tres Leches Cake');
    await searchBox.first().press('Enter');
  } else {
    // Fallback: try typing into the page and pressing Enter
    await page.keyboard.type('Tres Leches Cake');
    await page.keyboard.press('Enter');
  }

  // Wait for results page to load
  await page.waitForSelector('#search', { timeout: 10000 });

  // Basic assertion: there should be at least one result heading
  const headings = page.locator('#search h3');
  await expect(headings.first()).toBeVisible({ timeout: 5000 });

  // Optional: verify the URL indicates a Google search
  await expect(page).toHaveURL(/.*google.*search\?q=/i);
});
```