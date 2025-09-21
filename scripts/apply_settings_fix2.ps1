
# apply_settings_fix2.ps1 - Overwrite options_dialog.py and rerun settings smoke
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

# Ensure dirs exist
if (-not (Test-Path ".\base_app\ui")) { New-Item -ItemType Directory -Force ".\base_app\ui" | Out-Null }

# Overwrite file from extracted pack
Copy-Item -Force ".\base_app\ui\options_dialog.py" ".\base_app\ui\options_dialog.py" | Out-Null

# Run smoke
if (Test-Path ".\scripts\run_smokes_all.ps1") {
  pwsh ".\scripts\run_smokes_all.ps1" -Select s2_settings_smoke
} else {
  & pytest -q tests\smoke\s2_settings_smoke.py
}
