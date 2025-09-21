
# apply_s1s2.ps1 - Idempotent placement + run S1/S2 smokes
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app\core"
Ensure-Dir ".\tests\smoke"

# Run smokes
pwsh ".\scripts\run_smokes_s1s2.ps1"
