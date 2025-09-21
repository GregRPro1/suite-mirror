# post_update_alt.ps1 (fallback)
$ErrorActionPreference = "Stop"
$env:QT_QPA_PLATFORM="offscreen"
if (Test-Path ".\scripts\cleanup_tests.ps1") { & .\scripts\cleanup_tests.ps1 }
.\.venv\Scripts\python.exe -m pytest -q -n auto
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$OUTDIR = ".\_results"
if (!(Test-Path $OUTDIR)) { New-Item -ItemType Directory -Force $OUTDIR | Out-Null }
$OUT = "$OUTDIR\sprint_results_$ts.zip"
Compress-Archive -Path ".\projects\*", ".\tmp\logs\*", ".\tests\smoke\*" -DestinationPath $OUT -Force -ErrorAction SilentlyContinue
Write-Host "RESULTS: $OUT"
