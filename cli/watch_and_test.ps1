# Artemis CodexOps: Parallel Local Watcher & Visual Test Runner (PowerShell)

$watchPath = "artemis-codexops"
$logPath = "artemis-codexops/cli/watch_and_test.log"
$scriptToRun = "artemis-codexops/cli/auto_visual_test.ps1"
$services = @(
  "plugin-marketplace",
  "api-billing",
  "certificate-issuer",
  "affiliate-program",
  "pay-per-use",
  "white-label",
  "billing-invoicing",
  "live-events",
  "in-app_purchases",
  "auth"
)

Write-Host "Starting persistent watcher on $watchPath. All changes will trigger parallel visual test runs for all services."
Write-Host "Logs will be written to $logPath."

$fsw = New-Object IO.FileSystemWatcher $watchPath -Property @{
    IncludeSubdirectories = $true
    NotifyFilter = [IO.NotifyFilters]'FileName, LastWrite, DirectoryName'
    Filter = '*.*'
}

$action = {
    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$time] Change detected. Running parallel visual test scripts for all services..."
    Add-Content $logPath "[$time] Change detected. Running parallel visual test scripts for all services..."
    $jobs = @()
    foreach ($svc in $using:services) {
        $jobs += Start-Job -ScriptBlock {
            powershell -ExecutionPolicy Bypass -File $using:scriptToRun -Service $using:svc | Tee-Object -FilePath $using:logPath -Append
        }
    }
    Wait-Job -Job $jobs
    $jobs | ForEach-Object { Receive-Job -Job $_ }
}

Register-ObjectEvent $fsw Changed -Action $action
Register-ObjectEvent $fsw Created -Action $action
Register-ObjectEvent $fsw Deleted -Action $action
Register-ObjectEvent $fsw Renamed -Action $action

Write-Host "Watcher running. Press Ctrl+C to stop."
while ($true) { Start-Sleep -Seconds 10 }
