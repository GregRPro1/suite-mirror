
# run_smokes_all.ps1 - robust all-sprints runner (array-safe)
[CmdletBinding()]
param(
  [string[]]$Select = @()  # optional glob filters like 's1_', 's3_'
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
Ensure-Dir ".\_results"

$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$logTxt = ".\_results\smokes_all_$ts.txt"
$xml    = ".\_results\smokes_all_$ts.junit.xml"

# Get all smoke tests
$all = @(Get-ChildItem -Path "tests\smoke" -Filter "*.py" -File -Recurse | ForEach-Object { $_.FullName })

# Optional selection filter(s)
if (@($Select).Count -gt 0) {
  $sel = @()
  foreach($g in @($Select)){
    $sel += @($all | Where-Object { $_ -like ("*{0}*" -f $g) })
  }
  $targets = @($sel | Sort-Object -Unique)
} else {
  $targets = @($all)
}

if (@($targets).Count -eq 0) {
  Write-Warning "No smoke tests found."
  # Still emit empty artifacts for CI consistency
  '' | Out-File -FilePath $logTxt -Encoding utf8
  '' | Out-File -FilePath $xml -Encoding utf8
  $zip = ".\_results\smokes_all_$ts.zip"
  if (Test-Path $zip) { Remove-Item $zip -Force }
  Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force
  Write-Host ("RESULTS: {0}" -f $zip)
  exit 0
}

# Run pytest
& pytest -q @targets --junitxml "$xml" 2>&1 | Tee-Object -FilePath "$logTxt"
$exit = $LASTEXITCODE

# Zip artifacts
$zip = ".\_results\smokes_all_$ts.zip"
if (Test-Path $zip) { Remove-Item $zip -Force }
Compress-Archive -Path @("$logTxt", "$xml") -DestinationPath "$zip" -Force

Write-Host ("RESULTS: {0}" -f $zip)
exit $exit
