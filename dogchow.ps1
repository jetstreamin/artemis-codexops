Start-Process powershell -ArgumentList "-NoExit", "-Command", "python agents/master_builder.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python agents/ops_agent.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python agents/dashboard_api.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd web; python -m http.server 8080"
Start-Sleep -Seconds 3
Start-Process "http://localhost:8080/mesh_dashboard.html"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "powershell -ExecutionPolicy Bypass -File cli/watch_and_test.ps1"
