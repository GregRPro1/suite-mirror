
# run_configurator_gui.ps1 - launch the PyQt6 configurator GUI
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
.\.venv\Scripts\python.exe -m configurator.ui.app_gui
