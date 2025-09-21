
# apply_s3s6_enh.ps1 - place enhancements and run S3–S6 smokes
[CmdletBinding()]
param()
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo
Ensure-Dir ".\base_app\core"
Ensure-Dir ".\plugins\sample_hello"
Ensure-Dir ".\configurator"
Ensure-Dir ".\tests\smoke"
Ensure-Dir ".\_results"
Ensure-Dir ".\tmp\logs"

pwsh ".\scripts\run_smokes_s3s6_enh.ps1"
