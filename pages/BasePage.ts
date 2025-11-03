import { Page } from '@playwright/test';

export class BasePage {
  constructor(protected page: Page) {}

  async navigate(url: string) {
    await this.page.goto(url);
  }

  async getTitle(): Promise<string> {
    return await this.page.title();
  }

  async waitForTimeout(milliseconds: number) {
    await this.page.waitForTimeout(milliseconds);
  }
}
