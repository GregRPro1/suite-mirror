
# apply_hotfix_cancel_all.ps1 - apply cancel fix and run selected or all smokes
[CmdletBinding()]
param(
  [string[]]$Select = @('s3_jobs_logging_enh_smoke')
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

if (-not (Test-Path ".\scripts\run_smokes_all.ps1")) {
  Write-Warning "scripts\run_smokes_all.ps1 not found after extract."
} else {
  pwsh ".\scripts\run_smokes_all.ps1" -Select $Select
}
