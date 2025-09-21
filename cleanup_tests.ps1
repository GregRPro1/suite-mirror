param()
# Remove rogue test dirs and pycache
if (Test-Path ".\smoke") { Remove-Item ".\smoke" -Recurse -Force }
if (Test-Path ".\test_recorder_trace.py") { Remove-Item ".\test_recorder_trace.py" -Force }
Get-ChildItem -Recurse -Include __pycache__,*.pyc | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "Cleaned rogue tests and caches."
