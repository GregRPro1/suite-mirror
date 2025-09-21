param(
  [Parameter(Mandatory=$true)][string]$Name,
  [Parameter(Mandatory=$true)][string]$Profile
)
$ErrorActionPreference = "Stop"
$projDir = ".\projects\$Name"
if (-not (Test-Path $projDir)) { New-Item -ItemType Directory -Force $projDir | Out-Null }
$py = ".\.venv\Scripts\python.exe"
& $py -m configurator.cli.configure --profile $Profile --out $projDir
Write-Host "Project created at $projDir"