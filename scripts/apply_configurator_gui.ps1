[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir { param([string]$p) if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir '.\configurator\ui'
Ensure-Dir '.\scripts'
Ensure-Dir '.\tests\smoke'
Ensure-Dir '.\_results'

Copy-Item -Force '.\configurator\ui\app_gui.py' '.\configurator\ui\app_gui.py'
Copy-Item -Force '.\scripts\run_configurator_gui.ps1' '.\scripts\run_configurator_gui.ps1'

# Smoke (headless)
$py = '.\.venv\Scripts\python.exe'
if (-not (Test-Path $py)) { $py = 'python' }

$ts = Get-Date -Format 'yyyyMMdd_HHmmss'
$junit = '.\_results\smokes_configurator_gui_{0}.junit.xml' -f $ts
$zip   = '.\_results\smokes_configurator_gui_{0}.zip' -f $ts

$smokePath = '.\tests\smoke\s5_configurator_gui_smoke.py'
@'
import pathlib
from PyQt6 import QtWidgets
from configurator.ui.app_gui import ConfiguratorWindow

def test_configurator_gui_generate(tmp_path):
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    w = ConfiguratorWindow()
    out = tmp_path / "proj"
    w.outdir.setText(str(out))
    w._on_generate_clicked(run_after=False)
    proj_yaml = out / "project.yaml"
    assert proj_yaml.exists(), "project.yaml not created by CLI"
'@ | Set-Content -Encoding UTF8 $smokePath

$env:QT_QPA_PLATFORM = 'offscreen'
& $py -m pytest -q $smokePath --junitxml $junit

try { Compress-Archive -Path @($smokePath,$junit,'.\configurator\ui\app_gui.py') -DestinationPath $zip -Force } catch {}

Write-Host ('RESULTS: {0}' -f $zip)
