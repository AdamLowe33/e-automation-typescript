import { test, expect } from '@playwright/test';
import { LoginPage, HomePage } from '../pages';

test.describe('Login Tests', () => {
  let loginPage: LoginPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    await loginPage.navigate('/account/login');
  });

  test('should login successfully with valid credentials', async ({ page }) => {
    await loginPage.login('testuser', 'password123');
    
    const homePage = new HomePage(page);
    await expect(page).toHaveURL(/.*home/);
    expect(await homePage.isUserProfileVisible()).toBeTruthy();
    await page.close();
  });

  test('should show error message with invalid credentials', async ({ page }) => {
    await loginPage.login('invaliduser', 'wrongpassword');
    
    expect(await loginPage.isErrorVisible()).toBeTruthy();
    const errorMsg = await loginPage.getErrorMessage();
    expect(errorMsg).toContain('Invalid credentials');
    await page.close();
  });

  test('should have correct page title', async ({ page }) => {
    const title = await loginPage.getTitle();
    expect(title).toBe('Login Page');
    await page.close();
  });
});
