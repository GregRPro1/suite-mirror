
# apply_hotfix_jobs_configurator.ps1 - apply fixes and run all smokes
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

# Ensure dirs
$dirs = @(".\base_app\core", ".\configurator\cli", ".\_results", ".\tmp\logs")
foreach($d in $dirs){ if(-not (Test-Path $d)){ New-Item -ItemType Directory -Force -Path $d | Out-Null } }

# Run unified smokes
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1"
} else {
  Write-Warning "scripts\run_smokes_all.ps1 not found; run pytest manually."
}
