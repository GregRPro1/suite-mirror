
# run_smokes_s1s2.ps1 - execute S1/S2 smokes only
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
Ensure-Dir ".\_results"

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logTxt = ".\_results\smokes_s1s2_$ts.txt"
$xml    = ".\_results\smokes_s1s2_$ts.junit.xml"

$targets = @(
  "tests/smoke/s1_docking_layouts_smoke.py",
  "tests/smoke/s2_actions_palette_smoke.py"
) | Where-Object { Test-Path $_ }

& pytest -q @targets --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exit = $LASTEXITCODE

$zip = ".\_results\smokes_s1s2_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force

Write-Host ("RESULTS: {0}" -f $zip)
exit $exit
