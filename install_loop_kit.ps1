<#
SYNOPSIS
  Installs loop kit from local _kit folder into repo paths and bootstraps Git.
USAGE
  pwsh -ExecutionPolicy Bypass -File .\install_loop_kit.ps1
#>
$ErrorActionPreference = "Stop"
function Ensure-Dir($p) { if (-not (Test-Path $p)) { New-Item -ItemType Directory -Force $p | Out-Null } }
Ensure-Dir ".\scripts\ai"; Ensure-Dir "._ai"
Copy-Item ".\_kit\scripts\git_setup.ps1" ".\scripts\git_setup.ps1" -Force
Copy-Item ".\_kit\scripts\ai\apply_and_test.ps1" ".\scripts\ai\apply_and_test.ps1" -Force
Copy-Item ".\_kit\scripts\ai\patch_fallback.py" ".\scripts\ai\patch_fallback.py" -Force
Copy-Item ".\_kit\scripts\ai\test_matrix.ps1" ".\scripts\ai\test_matrix.ps1" -Force
Write-Host "Installing loop kit complete." -ForegroundColor Green
Write-Host "Bootstrapping Git..." -ForegroundColor Cyan
pwsh .\scripts\git_setup.ps1 -ShowStatus
