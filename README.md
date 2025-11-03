# E2E Automation with Playwright

A TypeScript-based Playwright test automation framework using the Page Object Model (POM) design pattern.

## Setup Instructions (Step-by-Step)

Here are all the commands used to set up this project from scratch:

### 1. Install Playwright and Dependencies

```bash
npm install --save-dev @playwright/test @types/node
```

### 2. Install Playwright Browsers

```bash
npx playwright install
```

### 3. Create Project Structure

```bash
mkdir -p tests pages fixtures
```

### 4. Files Created

The following files were created to set up the framework:

- `playwright.config.ts` - Playwright configuration with multi-browser support
- `pages/BasePage.ts` - Base page class with common methods
- `pages/LoginPage.ts` - Login page object example
- `pages/HomePage.ts` - Home page object example
- `pages/index.ts` - Export all page objects
- `tests/example.spec.ts` - Example test file
- `tests/login.spec.ts` - Login test file using POM
- `.gitignore` - Ignore node_modules, test results, etc.

### 5. Package.json Scripts Added

```json
"scripts": {
  "build": "tsc",
  "test": "playwright test",
  "test:ui": "playwright test --ui",
  "test:headed": "playwright test --headed",
  "test:debug": "playwright test --debug",
  "report": "playwright show-report"
}
```

## Project Structure

```
e-automation/
├── pages/              # Page Object Model classes
│   ├── BasePage.ts     # Base page with common methods
│   ├── LoginPage.ts    # Login page object
│   ├── HomePage.ts     # Home page object
│   └── index.ts        # Exports all page objects
├── tests/              # Test specifications
│   ├── example.spec.ts # Example tests
│   └── login.spec.ts   # Login tests
├── fixtures/           # Custom fixtures (if needed)
├── playwright.config.ts # Playwright configuration
└── package.json
```

## Running Tests

```bash
# Run all tests
npm test

# Run tests in UI mode
npm run test:ui

# Run tests in headed mode
npm run test:headed

# Debug tests
npm run test:debug

# View test report
npm run report
```

## Page Object Model

This framework uses the Page Object Model pattern to organize test code:

- **BasePage**: Contains common methods shared across all pages
- **Page Objects**: Represent individual pages with locators and actions
- **Tests**: Use page objects to interact with the application

## Example Usage

```typescript
import { test, expect } from '@playwright/test';
import { LoginPage, HomePage } from '../pages';

test('login test', async ({ page }) => {
  const loginPage = new LoginPage(page);
  await loginPage.navigate('/login');
  await loginPage.login('username', 'password');
  
  const homePage = new HomePage(page);
  expect(await homePage.isUserProfileVisible()).toBeTruthy();
});
```

## Creating New Page Objects

1. Create a new file in the `pages/` directory
2. Extend the `BasePage` class
3. Define locators as private readonly properties
4. Create methods for page interactions
5. Export the class in `pages/index.ts`

Example:

```typescript
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class MyPage extends BasePage {
  private readonly myButton: Locator;

  constructor(page: Page) {
    super(page);
    this.myButton = page.locator('#my-button');
  }

  async clickMyButton() {
    await this.myButton.click();
  }
}
```
