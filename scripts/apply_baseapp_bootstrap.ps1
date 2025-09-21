# apply_baseapp_bootstrap.ps1
# Idempotent apply for Suite base app smoke tests and helpers
# Usage (from repo root after extracting zip):
#   pwsh .\scripts\apply_baseapp_bootstrap.ps1
[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Ensure-Dir($path) {
  if (-not (Test-Path -LiteralPath $path)) {
    New-Item -ItemType Directory -Force -Path $path | Out-Null
  }
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $repoRoot

# Ensure target dirs exist
Ensure-Dir ".\scripts"
Ensure-Dir ".\tests\smoke"
Ensure-Dir ".\_results"

# Place our files (they are already extracted into the correct relative paths).
# To be explicit and idempotent, overwrite from the extracted payload beside this script.
$payloadRoot = $repoRoot  # files are already placed by Expand-Archive into repo root
$files = @(
  ".\scripts\run_smokes.ps1",
  ".\tests\smoke\docking_layouts_smoke.py",
  ".\tests\smoke\action_registry_smoke.py",
  ".\tests\smoke\jobs_logging_smoke.py",
  ".\tests\smoke\plugin_system_smoke.py",
  ".\tests\smoke\configurator_smoke.py",
  ".\tests\smoke\feedback_crash_smoke.py"
)

foreach ($f in $files) {
  if (-not (Test-Path $f)) {
    Write-Host "Deploying missing file: $f"
    # If missing (unexpected), copy from payload path relative to this script
    $src = (Join-Path $payloadRoot $f.TrimStart('.\'))
    if (Test-Path $src) {
      Copy-Item -Path $src -Destination $f -Force
    } else {
      # If source also missing, just warn; run_smokes will still handle gracefully.
      Write-Warning "Source not found for $f; continuing."
    }
  } else {
    # Already present from extraction; ensure file is writable (idempotent)
    (Get-Item $f).IsReadOnly = $false
  }
}

# Kick smokes
Write-Host "Running smoke tests..."
pwsh ".\scripts\run_smokes.ps1"
