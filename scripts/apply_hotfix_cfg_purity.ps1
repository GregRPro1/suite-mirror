
# apply_hotfix_cfg_purity.ps1 - overwrite configurator CLI with quote-safe version and rerun only s5 + config tests, then all
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s5_configurator_functional_test,test_configurator_
  pwsh ".\scripts\run_smokes_all.ps1"
} else {
  Write-Warning "scripts\run_smokes_all.ps1 not found; run pytest manually."
}
