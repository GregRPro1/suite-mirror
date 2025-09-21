# post_update.ps1 (param-free, ASCII-safe)
$ErrorActionPreference = "Stop"

Write-Host "Cleaning test state..."
if (Test-Path ".\scripts\cleanup_tests.ps1") {
  & .\scripts\cleanup_tests.ps1
}

# Purge caches defensively
Get-ChildItem -Recurse -Force -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Force -Include *.pyc | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "Running smoke tests..."
$env:QT_QPA_PLATFORM="offscreen"
.\.venv\Scripts\python.exe -m pytest -q -n auto

# Package results
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OUTDIR = ".\_results"
if (!(Test-Path $OUTDIR)) { New-Item -ItemType Directory -Force $OUTDIR | Out-Null }
$OUT = "$OUTDIR\sprint_results_$ts.zip"

# Include projects (incl. inbox zips), tmp logs, and tests/smoke sources
$paths = @(".\projects", ".\tmp\logs", ".\tests\smoke")
$include = @()
foreach ($p in $paths) {
  if (Test-Path $p) { $include += (Join-Path $p "*") }
}

Compress-Archive -Path $include -DestinationPath $OUT -Force
Write-Host "RESULTS: $OUT"
