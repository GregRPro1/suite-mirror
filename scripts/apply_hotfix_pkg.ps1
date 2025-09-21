
# apply_hotfix_pkg.ps1 - make base_app importable and re-run S3–S6 smokes
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app\core"
Ensure-Dir ".\tests"

# Place files (already extracted); just ensure not read-only
foreach($f in @(".\base_app\__init__.py", ".\base_app\core\__init__.py", ".\tests\conftest.py")){
  if (-not (Test-Path $f)) {
    $src = Join-Path $repo $f.TrimStart(".\")
    if (Test-Path $src) { Copy-Item $src $f -Force }
  }
  if (Test-Path $f) { (Get-Item $f).IsReadOnly = $false }
}

# Re-run S3–S6 smokes
if (Test-Path ".\scripts\run_smokes_s3s6.ps1") {
  pwsh ".\scripts\run_smokes_s3s6.ps1"
} else {
  Write-Warning "scripts\\run_smokes_s3s6.ps1 not found; nothing to run."
}
