param()
$ErrorActionPreference = "Stop"

function Get-PyCmd {
  if (Get-Command py -ErrorAction SilentlyContinue) { return "py -3.12" }
  if (Get-Command python -ErrorAction SilentlyContinue) { return "python" }
  return $null
}

$pycmd = Get-PyCmd
if (-not $pycmd) {
  Write-Error @"
No suitable Python runtime found.
Install Python 3.12 (recommended) or 3.11, e.g.:
  winget install --id Python.Python.3.12 -e
Then re-run:  pwsh .\scripts\bootstrap.ps1
"@
  exit 1
}

$venv = ".\.venv"
if (-not (Test-Path $venv)) {
  Write-Host "Creating venv with: $pycmd -m venv .venv"
  & $pycmd -m venv .venv
}

$py = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
  Write-Error "Virtualenv Python not found at $py"
  exit 1
}

& $py -m pip install --upgrade pip
& $py -m pip install pyqt6 pyyaml jsonschema pytest pytest-xdist

Write-Host "OK: venv ready. Activate with: `".\.venv\Scripts\Activate.ps1`""
