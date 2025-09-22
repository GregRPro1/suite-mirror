[CmdletBinding()]
param([switch]$Headless)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

$py = '.\.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }

if ($Headless) { $env:QT_QPA_PLATFORM = 'offscreen' }
& $py -m configurator.ui.app_gui
