
# apply_hotfix_v3.ps1 - force-place files and run failing buckets then all
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app\core"
Ensure-Dir ".\configurator\cli"
Ensure-Dir ".\_results"
Ensure-Dir ".\tmp\logs"

# Run focused tests first for speed
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s3_jobs_logging_enh_smoke,test_configurator_,s5_configurator_functional_test,test_feedback_fileshare
  pwsh ".\scripts\run_smokes_all.ps1"
} else {
  Write-Warning "scripts\run_smokes_all.ps1 missing; run pytest manually."
}
