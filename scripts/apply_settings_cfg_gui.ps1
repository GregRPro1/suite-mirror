
# apply_settings_cfg_gui.ps1 - place files and run settings/configurator GUI smokes
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app\core"
Ensure-Dir ".\base_app\ui"
Ensure-Dir ".\configurator\ui"
Ensure-Dir ".\tests\smoke"
Ensure-Dir ".\_results"

if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s2_settings_smoke
} else {
  & pytest -q tests/smoke/s2_settings_smoke.py
}

