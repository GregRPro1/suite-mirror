
# apply_demo_pack.ps1 - place demo files and offer smoke + demo commands
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app"
Ensure-Dir ".\scripts"
Ensure-Dir ".\_results"

Write-Host "Demo pack applied."
Write-Host "Run headless demo:"
Write-Host "  pwsh .\scripts\run_demo.ps1 -Headless"
Write-Host "Run GUI demo:"
Write-Host "  pwsh .\scripts\run_demo.ps1"
