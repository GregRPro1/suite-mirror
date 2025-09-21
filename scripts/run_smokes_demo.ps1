
# run_smokes_demo.ps1 - run demo end-to-end smoke and zip results
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
Ensure-Dir ".\_results"

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logTxt = ".\_results\smokes_demo_$ts.txt"
$xml    = ".\_results\smokes_demo_$ts.junit.xml"

& pytest -q tests/smoke/demo_end_to_end_smoke.py --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exit = $LASTEXITCODE

$zip = ".\_results\smokes_demo_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force

Write-Host ("RESULTS: {0}" -f $zip)
exit $exit
