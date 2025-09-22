[CmdletBinding()]
param()
$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$dest = Join-Path "." "scripts\sync_mirror_now.ps1"
$destDir = Split-Path -Parent $dest
if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Force $destDir | Out-Null }

# Write the script content directly to avoid self-copy issues
$contents = @'
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
'@

Set-Content -Encoding UTF8 -NoNewline -Path $dest -Value $contents

Write-Host "Installed: $dest"
Write-Host "Usage: pwsh .\scripts\sync_mirror_now.ps1"
