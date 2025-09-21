
# apply_hotfix_s1_enum.ps1 - fix PyQt6 enum usage and re-run S1/S2 smokes
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

# Re-run S1/S2 smokes
if (Test-Path ".\scripts\run_smokes_s1s2.ps1") {
  pwsh ".\scripts\run_smokes_s1s2.ps1"
} else {
  Write-Warning "scripts\run_smokes_s1s2.ps1 not found."
}
