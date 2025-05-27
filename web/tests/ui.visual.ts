import { test, expect } from '@playwright/test';

test.use({ headless: false }); // Run in headed mode to show browser

test('Visual: Dashboard renders and is interactive', async ({ page }) => {
  await page.goto('http://localhost:8080/web/index.html');
  await page.waitForTimeout(1000); // Let the UI load

  // Interact with chat
  await page.fill('#chat-input', 'Visual test message');
  await page.click('button:has-text("Send")');
  await page.waitForTimeout(1000);

  // Click premium features link
  await page.click('a[href="premium.html"]');
  await page.waitForTimeout(1000);

  // Go back to dashboard
  await page.goBack();
  await page.waitForTimeout(500);

  // Click analytics link
  await page.click('a[href="analytics.html"]');
  await page.waitForTimeout(1000);

  // Go back to dashboard
  await page.goBack();
  await page.waitForTimeout(500);

  // Click live events link
  await page.click('a[href="events.html"]');
  await page.waitForTimeout(1000);

  // Go back to dashboard
  await page.goBack();
  await page.waitForTimeout(500);

  // Click white-label link
  await page.click('a[href="whitelabel.html"]');
  await page.waitForTimeout(1000);

  // Go back to dashboard
  await page.goBack();
  await page.waitForTimeout(500);

  // Pause for manual inspection
  await page.waitForTimeout(3000);
});
