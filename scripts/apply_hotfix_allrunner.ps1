
# apply_hotfix_allrunner.ps1 - place fixed runner and execute
[CmdletBinding()]
param(
  [string[]]$Select = @()  # pass-through to run_smokes_all.ps1
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

if (-not (Test-Path ".\scripts\run_smokes_all.ps1")) {
  Write-Warning "run_smokes_all.ps1 not found after extraction."
} else {
  if (@($Select).Count -gt 0) {
    pwsh ".\scripts\run_smokes_all.ps1" -Select $Select
  } else {
    pwsh ".\scripts\run_smokes_all.ps1"
  }
}
