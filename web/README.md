# Artemis CodexOps Web Dashboard

## 🚀 Frictionless Onboarding

### VR/WebXR & Airsupport Deployment

- The dashboard supports both standard web and VR/WebXR modes.
- Use the "Switch to VR Mode" button (top right) to enter immersive VR mode (WebXR, Quest browser, etc.).
- Use the "Switch to Web Mode" button in VR to return to the standard dashboard.
- No install required: works instantly on GitHub Pages, Quest browser, and any WebXR-compatible device.

### One-Click Deploy

- **Deploy to AWS (ECS/Fargate Free Tier):**
  1. Fork this repo and clone it.
  2. Update `cloudformation-template.yaml` with your AWS defaults or use the provided sample image and default VPC/subnet/security group.
  3. Push to GitHub and let the included GitHub Actions workflow auto-deploy.

- **Live Demo / Sandbox:**
  - [Try the dashboard live on GitHub Pages](https://jetstreamin.github.io/artemis-codexops/web/index.html)
  - No login or credit card required for demo.

- **Interactive Tutorial:**
  - Coming soon: In-app onboarding and sample data for new users.

---

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
