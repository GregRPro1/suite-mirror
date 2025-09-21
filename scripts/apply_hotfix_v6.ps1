
# apply_hotfix_v6.ps1 - write ui.window.default_size and re-run failing test then all
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select test_configurator_outputs_yaml_with_theme
  pwsh ".\scripts\run_smokes_all.ps1"
} else {
  Write-Warning "scripts\run_smokes_all.ps1 not found; run pytest manually."
}
