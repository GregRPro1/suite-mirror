param([string]$PatchPath = "._ai\last.patch", [switch]$LaunchIfGreen)
$ErrorActionPreference = "Stop"
function Exec($cmd) {
  Write-Host "» $cmd" -ForegroundColor Cyan
  & $env:ComSpec /c $cmd 2>&1 | ForEach-Object { $_.TrimEnd() } | ForEach-Object { if($_){ Write-Host $_ } }
  if ($LASTEXITCODE -ne 0) { throw "Command failed: $cmd" }
}
if (-not (Test-Path $PatchPath)) { throw "Patch file not found: $PatchPath" }
if (Get-Command git -ErrorAction SilentlyContinue) {
  Write-Host "Applying patch with git..." -ForegroundColor Green
  Exec "git apply --whitespace=nowarn `"$PatchPath`""
} else {
  Write-Host "git not found; using Python fallback..." -ForegroundColor Yellow
  if (-not (Test-Path .\.venv\Scripts\python.exe)) { throw "No Python venv found at .\.venv" }
  .\.venv\Scripts\python.exe .\scripts\ai\patch_fallback.py
  if ($LASTEXITCODE -ne 0) { throw "Patch fallback failed." }
}
if (Test-Path .\scripts\post_update.ps1) {
  pwsh .\scripts\post_update.ps1
} else {
  Write-Host "WARN: scripts\post_update.ps1 not found; running bare pytest" -ForegroundColor Yellow
  .\.venv\Scripts\python.exe -m pytest -q -n auto
}
if ($LaunchIfGreen) {
  if (Test-Path .\projects\barsim_demo\project.yaml) {
    .\.venv\Scripts\python.exe -m base_app --project .\projects\barsim_demo
  } else {
    .\.venv\Scripts\python.exe -m base_app
  }
}
