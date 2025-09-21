# Loop Kit v5 (Git + Patch + Matrix)
Install (repo root):
  Expand-Archive -Path "$HOME\Downloads\loop_kit_v5.zip" -DestinationPath "." -Force
  pwsh -ExecutionPolicy Bypass -File .\install_loop_kit.ps1

Apply patches:
  Save diff to ._ai\last.patch then:
  pwsh .\scripts\ai\apply_and_test.ps1 -LaunchIfGreen

Run subset smokes:
  pwsh .\scripts\ai\test_matrix.ps1 -Markers "theme,docking"
