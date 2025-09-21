$ErrorActionPreference = "Stop"
$env:QT_QPA_PLATFORM="offscreen"
.\.venv\Scripts\python.exe -m pytest -q -n auto