// File: tests/google-search.spec.ts
import { test, expect } from '@playwright/test';

test('Navigate to Google and search for Tres Leches Cake', async ({ page }) => {
  // Go to Google
  await page.goto('https://www.google.com');

  // Try to dismiss cookie/consent dialog if it appears (varies by region/language)
  const consentButton = page.locator('button', { hasText: /I agree|Accept|Continuar|Aceitar|Akzeptieren/i });
  if (await consentButton.count() > 0) {
    await consentButton.first().click();
  }

  // Ensure the search box is visible
  const searchBox = page.locator('input[name="q"]');
  await searchBox.waitFor({ state: 'visible' });

  // Type the query and search
  await searchBox.fill('Tres Leches Cake');
  await page.keyboard.press('Enter');

  // Wait for the results page and verify the query is in the URL
  await expect(page).toHaveURL(/q=Tres%20Leches%20Cake/);

  // Basic validation that results are shown
  const resultsContainer = page.locator('#search');
  await expect(resultsContainer).toBeVisible();

  // Optional: verify the title contains the search term
  await expect(page).toHaveTitle(/Tres Leches Cake|Google Search/);
});