# Suite Skeleton

## Quick start
```powershell
pwsh .\scripts\bootstrap.ps1
pwsh .\scripts\new_project.ps1 -Name barsim_demo -Profile barsim
pwsh .\scripts\run_tests.ps1
python -m base_app.core.app_bootstrap --project .\projects\barsim_demo\project.yaml