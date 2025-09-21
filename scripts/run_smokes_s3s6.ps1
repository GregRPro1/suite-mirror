
# run_smokes_s3s6.ps1 - execute S3–S6 smokes only
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
Ensure-Dir ".\_results"

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logTxt = ".\_results\smokes_s3s6_$ts.txt"
$xml    = ".\_results\smokes_s3s6_$ts.junit.xml"

$targets = @(
  "tests/smoke/s3_jobs_logging_functional_test.py",
  "tests/smoke/s4_plugin_system_functional_test.py",
  "tests/smoke/s5_configurator_functional_test.py",
  "tests/smoke/s6_feedback_crash_functional_test.py"
) | Where-Object { Test-Path $_ }

if ($targets.Count -eq 0) {
  Write-Warning "No S3–S6 smoke targets found."
  exit 0
}

& pytest -q @targets --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exit = $LASTEXITCODE

$zip = ".\_results\smokes_s3s6_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force

Write-Host ("RESULTS: {0}" -f $zip)
exit $exit
