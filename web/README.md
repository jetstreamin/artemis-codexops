# Artemis CodexOps Web Dashboard

## Automated UI Testing

This project uses [Playwright](https://playwright.dev/) for end-to-end automated testing of the dashboard UI.

### Running Tests

1. Install dependencies:
   ```
   npm install
   ```
2. Run the test suite:
   ```
   npm test
   ```

### Test Artifacts

- Playwright will generate test reports, screenshots, and videos for each test run.
- Artifacts can be published to GitHub Pages for live review of all UI states and flows.

### CI Integration

- Add the following to your GitHub Actions workflow to run tests and upload artifacts:
  ```yaml
  - name: Install dependencies
    run: npm install --prefix artemis-codexops/web
  - name: Run Playwright tests
    run: npm test --prefix artemis-codexops/web
  - name: Upload Playwright report
    uses: actions/upload-artifact@v3
    with:
      name: playwright-report
      path: artemis-codexops/web/playwright-report/
  ```

## Additional Notes

- For local development, ensure the dashboard is served at http://localhost:8080/web/index.html or update the test URLs accordingly.
- For more information, see [Playwright documentation](https://playwright.dev/).
