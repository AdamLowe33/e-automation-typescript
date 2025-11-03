import { test, expect } from '@playwright/test';

test.describe('Example Tests', () => {
  test('basic test example', async ({ page }) => {
    await page.goto('https://playwright.dev/');
    
    const title = await page.title();
    expect(title).toContain('Playwright');
  });

  test('has get started link', async ({ page }) => {
    await page.goto('https://playwright.dev/');

    await page.getByRole('link', { name: 'Get started' }).click();
    await expect(page).toHaveURL(/.*intro/);
  });
});
