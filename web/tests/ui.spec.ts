import { test, expect } from '@playwright/test';

test.describe('Artemis CodexOps Dashboard UI', () => {
  test('should display header, mesh chart, chat, and live log', async ({ page }) => {
    await page.goto('http://localhost:8080/web/index.html');

    // Header
    await expect(page.locator('h1')).toHaveText(/Artemis CodexOps/i);

    // Mesh chart
    await expect(page.locator('.main-chart h2')).toHaveText(/Distributed Mesh Network/i);
    await expect(page.locator('#mesh-chart')).toBeVisible();

    // Chat window
    await expect(page.locator('.chat-window h2')).toHaveText(/Live Chat/i);
    await expect(page.locator('#chat-messages')).toBeVisible();
    await expect(page.locator('#chat-input')).toBeVisible();

    // Live log
    await expect(page.locator('.live-log h2')).toHaveText(/Live Agent Log/i);
    await expect(page.locator('#log-list')).toBeVisible();
  });

  test('should allow sending a chat message', async ({ page }) => {
    await page.goto('http://localhost:8080/web/index.html');
    const input = page.locator('#chat-input');
    const sendBtn = page.locator('button', { hasText: 'Send' });

    await input.fill('Test message');
    await sendBtn.click();

    await expect(page.locator('#chat-messages')).toContainText('Test message');
  });

  test('should display simulated log entries', async ({ page }) => {
    await page.goto('http://localhost:8080/web/index.html');
    // Wait for at least one simulated log entry to appear
    await expect(page.locator('#log-list')).toContainText('Agent event: mesh update');
  });
});
