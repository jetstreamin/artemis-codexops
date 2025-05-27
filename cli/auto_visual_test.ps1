# Artemis CodexOps: Automated Local Visual Test & Self-Heal Loop (PowerShell)

$maxIter = 50
$iter = 1

while ($iter -le $maxIter) {
  Write-Host "=== Iteration $iter/$maxIter ==="

  # 1. Start local web server (if not already running)
  $webServer = Start-Process -FilePath "python" -ArgumentList "-m http.server 8080" -WorkingDirectory "artemis-codexops/web" -PassThru
  Start-Sleep -Seconds 2

  # 2. Run Playwright UI tests in headed mode
  Write-Host "Running Playwright UI visual tests..."
  cd artemis-codexops/web
  npm install
  npx playwright test tests/ui.visual.ts > ..\web\test-results\ui-visual.log 2>&1
  cd ../..

  # 3. Run CLI/TUI tests
  Write-Host "Running CLI/TUI tests..."
  pip install pexpect
  python artemis-codexops/cli/test_tui.py > artemis-codexops/cli/tui-test.log 2>&1

  # 4. Parse test results for errors
  $uiLog = Get-Content artemis-codexops/web/test-results/ui-visual.log -Raw
  $tuiLog = Get-Content artemis-codexops/cli/tui-test.log -Raw

  if ($uiLog -match "FAIL|Error|Exception" -or $tuiLog -match "FAIL|Error|Exception") {
    Write-Host "Test errors detected. Attempting auto-fix..."

    # Auto-fix: npm audit fix, npm install, reformat, restart server
    cd artemis-codexops/web
    npm audit fix
    npm install
    cd ../..

    # Optionally, run a code formatter or linter here

    # Kill and restart web server
    Stop-Process -Id $webServer.Id -Force
    Start-Sleep -Seconds 2
    $iter++
    continue
  }

  # 5. If all tests pass, stop web server and exit
  Write-Host "All tests passed and UI is visually confirmed."
  Stop-Process -Id $webServer.Id -Force
  exit 0
}

Write-Host "Max iterations reached. Some tests or deployments may still be failing."
exit 1
