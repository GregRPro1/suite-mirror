[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir { param([string]$p) if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $repo

Ensure-Dir '.\tools\py'
Ensure-Dir '.\tests\smoke'
Ensure-Dir '.\_results'
Ensure-Dir '.\_packs'

$py = '.\.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }

& $py '.\tools\py\patch_settings_menu.py'

$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$junit = '.\_results\smokes_settings_menu_{0}.junit.xml' -f $ts
$zip   = '.\_results\smokes_settings_menu_{0}.zip' -f $ts

& $py -m pytest -q tests\smoke\s2_settings_menu_wiring_smoke.py --junitxml $junit

try {
  Compress-Archive -Path @('main_window.py', $junit, '.\tools\py\patch_settings_menu.py') -DestinationPath $zip -Force
} catch { Write-Warning $_ }

Write-Host ('RESULTS: {0}' -f $zip)
