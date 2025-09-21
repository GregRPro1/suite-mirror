
# run_smokes_settings.ps1 - run only settings-related smokes
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s2_settings_smoke
} else {
  & pytest -q tests/smoke/s2_settings_smoke.py
}
