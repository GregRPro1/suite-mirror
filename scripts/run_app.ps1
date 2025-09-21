
param(
  [string]$Project = ".\projects\barsim_demo"
)
$python = ".\.venv\Scripts\python.exe"
& $python -m base_app --project $Project
