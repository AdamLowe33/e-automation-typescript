import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  private readonly welcomeMessage: Locator;
  private readonly logoutButton: Locator;
  private readonly userProfile: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeMessage = page.locator('.welcome-message');
    this.logoutButton = page.locator('#logout');
    this.userProfile = page.locator('.user-profile');
  }

  async getWelcomeMessage(): Promise<string> {
    return await this.welcomeMessage.textContent() || '';
  }

  async logout() {
    await this.logoutButton.click();
  }

  async isUserProfileVisible(): Promise<boolean> {
    return await this.userProfile.isVisible();
  }
}
