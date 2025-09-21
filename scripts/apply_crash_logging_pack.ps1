
# apply_crash_logging_pack.ps1
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo
Ensure-Dir ".\base_app\core"
Ensure-Dir ".\tests\smoke"
Ensure-Dir ".\_results\crash"

if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s6_crash_logging_smoke
} else {
  & pytest -q tests\smoke\s6_crash_logging_smoke.py
}
