
# apply_hotfix_v2.ps1 - apply v2 fixes and run focused smokes first
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

# Focus failing buckets first
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s3_jobs_logging_enh_smoke,test_configurator_,s5_configurator_functional_test,test_feedback_fileshare
  # Then run all
  pwsh ".\scripts\run_smokes_all.ps1"
} else {
  Write-Warning "scripts\run_smokes_all.ps1 not found; run pytest manually."
}
