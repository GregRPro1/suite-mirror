
# run_demo.ps1 - Generate a demo project via configurator CLI and launch the app
[CmdletBinding()]
param(
  [string]$Profile = "barsim",
  [string]$OutDir = ".\_demo\proj",
  [string]$BaseColor = "#0b3d91",
  [string]$AccentColor = "#ffcc00",
  [int]$Width = 1400,
  [int]$Height = 900,
  [switch]$Maximized,
  [string]$Layout = "wide-right",
  [string]$Panels = "ProjectExplorer,Jobs,Logs,Settings",
  [switch]$Headless
)
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir $OutDir
# 1) Generate project via configurator (module runner)
$py = ".\.venv\Scripts\python.exe"
$cfgArgs = @(
  "-m","configurator.cli.configure",
  "--profile",$Profile,"--out",$OutDir,
  "--brand-base-color",$BaseColor,
  "--brand-accent-color",$AccentColor,
  "--window-width",$Width.ToString(),
  "--window-height",$Height.ToString(),
  "--window-maximized","false",
  "--layout",$Layout,"--panels",$Panels
)
& $py @cfgArgs

# 2) Launch demo app (headless or GUI)
$demoArgs = @("--project",$OutDir,"--profile",$Profile)
if ($Headless) { $demoArgs += "--headless" }
& $py "-m" "base_app.demo_app" @demoArgs
