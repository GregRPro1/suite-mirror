
# apply_s3s6.ps1 - Idempotent placement + run smokes for S3–S6
[CmdletBinding()]
param()
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($p){ if(-not (Test-Path $p)){ New-Item -ItemType Directory -Force -Path $p | Out-Null } }

$repo = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repo

Ensure-Dir ".\base_app\core"
Ensure-Dir ".\plugins\sample_hello"
Ensure-Dir ".\configurator"
Ensure-Dir ".\ui\qss"
Ensure-Dir ".\_results"
Ensure-Dir ".\tmp\logs"
Ensure-Dir ".\tests\smoke"

# Files already extracted into place by Expand-Archive.
# Run smokes
pwsh ".\scripts\run_smokes_s3s6.ps1"
