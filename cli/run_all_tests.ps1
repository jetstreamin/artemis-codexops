# Artemis CodexOps: Run All Tests (UI, TUI, API) on Windows

Write-Host "=== Running Playwright UI tests ==="
cd artemis-codexops/web
npm install
npm test
cd ../..

Write-Host "=== Running TUI/CLI tests ==="
pip install pexpect
python artemis-codexops/cli/test_tui.py

Write-Host "=== All tests complete. Check above for results and errors."
