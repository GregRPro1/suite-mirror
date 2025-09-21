<#
SYNOPSIS
  One-time Git bootstrap & branch helper.
USAGE
  pwsh .\scripts\git_setup.ps1 -ShowStatus
  pwsh .\scripts\git_setup.ps1 -CreateBranch feat/theme-apply-qss
#>
param(
  [string]$CreateBranch = "",
  [switch]$ProtectMain,
  [switch]$ShowStatus
)
$ErrorActionPreference = "Stop"
function Exec($cmd) {
  Write-Host "» $cmd" -ForegroundColor Cyan
  & $env:ComSpec /c $cmd 2>&1 | ForEach-Object { $_.TrimEnd() } | ForEach-Object { if($_){ Write-Host $_ } }
  if ($LASTEXITCODE -ne 0) { throw "Command failed: $cmd" }
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git not found in PATH. Install Git for Windows first." }
if (-not (Test-Path .git)) { Exec "git init" }
if (-not (git config user.name))  { Exec 'git config user.name "Suite Dev"' }
if (-not (git config user.email)) { Exec 'git config user.email "dev@example.com"' }
$cur = ""; try { $cur = (git rev-parse --abbrev-ref HEAD).Trim() } catch {}
if (-not $cur) { Exec "git checkout -b main" }
$has_commits = $false; try { git rev-parse --verify HEAD *> $null; $has_commits = $true } catch { $has_commits = $false }
if (-not $has_commits) { Exec "git add -A"; Exec 'git commit -m "chore(repo): baseline after initial sprints"' }
if ($CreateBranch) { Exec "git checkout -b $CreateBranch" }
if ($ProtectMain) {
  Write-Host "`nProtect 'main' on your remote:" -ForegroundColor Yellow
  Write-Host " - Require PRs + status checks (smoke matrix), 1 reviewer"
  Write-Host " - Disallow force-push & direct pushes"
}
if ($ShowStatus) { Exec "git status -sb"; Exec "git log --oneline -n 5" }
