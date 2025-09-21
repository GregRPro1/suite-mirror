param([string]$Markers = "theme,docking,palette,plugins,jobs_logs,configurator_gui")
$ErrorActionPreference = "Stop"
$markers = $Markers.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
foreach ($m in $markers) {
  Write-Host "`n=== Running marker: $m ===" -ForegroundColor Green
  .\.venv\Scripts\python.exe -m pytest -q -n auto -m $m
  if ($LASTEXITCODE -ne 0) { Write-Host "Marker failed: $m" -ForegroundColor Red; break }
}
