$ErrorActionPreference = "Stop"
$env:QT_QPA_PLATFORM="offscreen"

Write-Host "Cleaning test state..."
if (Test-Path ".\scripts\cleanup_tests.ps1") { & .\scripts\cleanup_tests.ps1 }

Write-Host "Running smoke tests..."
.\.venv\Scripts\python.exe -m pytest -q -n auto

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OUTDIR = ".\_results"
if (!(Test-Path $OUTDIR)) { New-Item -ItemType Directory -Force $OUTDIR | Out-Null }
$OUT = "$OUTDIR\sprint_results_$ts.zip"

$paths = @(".\projects", ".\tmp\logs", ".\tests\smoke")
$include = @()
foreach ($p in $paths) { if (Test-Path $p) { $include += (Join-Path $p "*") } }
if ($include.Count -eq 0) { $include = @(".") }  # never fail
Compress-Archive -Path $include -DestinationPath $OUT -Force
Write-Host "RESULTS: $OUT"
