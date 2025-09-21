
# apply_settings_hotfix_import.ps1 - fix options_dialog import and rerun settings smoke
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Copy-Item -Force ".\scripts\..\base_app\ui\options_dialog.py" ".\base_app\ui\options_dialog.py"

if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s2_settings_smoke
} else {
  & pytest -q tests/smoke/s2_settings_smoke.py
}
