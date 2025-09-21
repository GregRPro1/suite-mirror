
# apply_ui_menubar_tabs.ps1 - place updated UI with menus/toolbars and run smoke
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo
Ensure-Dir ".\base_app\core\panels"
Ensure-Dir ".\tests\smoke"
Ensure-Dir ".\_results"

# Run the new smoke (plus keep global runner available if present)
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s1_tabs_menu_smoke
} else {
  & pytest -q tests/smoke/s1_tabs_menu_smoke.py
}

