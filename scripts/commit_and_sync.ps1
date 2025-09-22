[CmdletBinding()]
param([string]$Message = "feat(configurator): GUI with color pickers, logo picker, generate & run")
$ErrorActionPreference='Stop'
Set-StrictMode -Version Latest
$branch = (git rev-parse --abbrev-ref HEAD).Trim()
git add -A
git commit -m $Message
if (-not (git remote | Select-String -SimpleMatch "mirror")) {
  git remote add mirror https://github.com/GregRPro1/suite-mirror.git
}
git push -u origin $branch
git push -u mirror $branch
