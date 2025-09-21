
# run_smokes_s3s6_enh.ps1 - run S3–S6 enhancement smokes
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
Ensure-Dir ".\_results"

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logTxt = ".\_results\smokes_s3s6_enh_$ts.txt"
$xml    = ".\_results\smokes_s3s6_enh_$ts.junit.xml"

$targets = @(
  "tests/smoke/s3_jobs_logging_enh_smoke.py",
  "tests/smoke/s4_plugin_meta_smoke.py",
  "tests/smoke/s5_config_gui_smoke.py",
  "tests/smoke/s6_feedback_transport_smoke.py"
) | Where-Object { Test-Path $_ }

& pytest -q @targets --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exit = $LASTEXITCODE

$zip = ".\_results\smokes_s3s6_enh_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force
Write-Host ("RESULTS: {0}" -f $zip)
exit $exit
