# run_smokes.ps1 - executes Suite base app parallel sprint smokes
[CmdletBinding()]
param(
  [string]$Marker = "smoke"
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($path) {
  if (-not (Test-Path -LiteralPath $path)) {
    New-Item -ItemType Directory -Force -Path $path | Out-Null
  }
}

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
Ensure-Dir ".\_results"

$logTxt = ".\_results\smokes_$ts.txt"
$xml    = ".\_results\smokes_$ts.junit.xml"

# Prefer venv python/pytest if available
$pytest = "pytest"

# Build a focused test selection that won't fail if user code isn't fully implemented yet.
$targets = @(
  "tests/smoke/docking_layouts_smoke.py",
  "tests/smoke/action_registry_smoke.py",
  "tests/smoke/jobs_logging_smoke.py",
  "tests/smoke/plugin_system_smoke.py",
  "tests/smoke/configurator_smoke.py",
  "tests/smoke/feedback_crash_smoke.py"
) | Where-Object { Test-Path $_ }

if ($targets.Count -eq 0) {
  Write-Warning "No smoke test targets found under tests/smoke. Exiting."
  exit 0
}

# Run pytest quietly, emit JUnit XML, and tee stdout
$cmd = @($pytest, "-q") + $targets + @("--junitxml", $xml)
Write-Host "pytest command: $($cmd -join ' ')"

# Run and capture output; don't throw on non-zero to allow zipping results
$LASTEXITCODE = 0
& $pytest -q @targets --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exitCode = $LASTEXITCODE

# Zip results
$zipPath = ".\_results\smokes_$ts.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zipPath" -Force

Write-Host ("RESULTS: {0}" -f $zipPath)
exit $exitCode
