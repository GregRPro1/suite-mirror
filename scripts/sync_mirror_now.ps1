[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$branch = (git rev-parse --abbrev-ref HEAD).Trim()
if (-not $branch -or $branch -eq "HEAD") {
  throw "Cannot determine current branch."
}

if (-not (git remote | Select-String -SimpleMatch "mirror")) {
  git remote add mirror https://github.com/GregRPro1/suite-mirror.git
}

Write-Host "Pushing ''$branch'' to origin..."
git push -u origin $branch

Write-Host "Pushing ''$branch'' to mirror..."
git push -u mirror $branch

Write-Host "Done. Both remotes synced for branch ''$branch''."