<#
.SYNOPSIS
  Installs oleander skills and workflows into the Claude Code skills directory.
.DESCRIPTION
  Default: creates directory junctions (no admin needed), so edits in this repo are live.
  -Copy      copy folders instead of linking
  -Uninstall remove only entries that this repo installed
  -Target    install directory (default: ~/.claude/skills)
#>
param(
    [switch]$Copy,
    [switch]$Uninstall,
    [string]$Target = (Join-Path $HOME '.claude\skills')
)

$ErrorActionPreference = 'Stop'
$sources = @('skills', 'workflows') |
    ForEach-Object { Join-Path $PSScriptRoot $_ } |
    Where-Object { Test-Path $_ } |
    ForEach-Object { Get-ChildItem $_ -Directory } |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }

$dupes = $sources | Group-Object Name | Where-Object Count -gt 1
if ($dupes) { throw "Duplicate names across skills/ and workflows/: $($dupes.Name -join ', ')" }

New-Item -ItemType Directory -Force $Target | Out-Null

foreach ($src in $sources) {
    $dest = Join-Path $Target $src.Name
    $existing = Get-Item $dest -Force -ErrorAction SilentlyContinue
    $isOurLink = $existing -and $existing.LinkType -and ($existing.Target -contains $src.FullName)
    $isOurCopy = $existing -and -not $existing.LinkType -and (Test-Path (Join-Path $dest '.oleander'))

    if ($Uninstall) {
        if ($isOurLink) { $existing.Delete(); Write-Host "removed  $($src.Name)" }
        elseif ($isOurCopy) { Remove-Item $dest -Recurse -Force; Write-Host "removed  $($src.Name)" }
        continue
    }

    if ($existing -and -not ($isOurLink -or $isOurCopy)) {
        Write-Warning "skip     $($src.Name): $dest exists and was not installed by this repo"
        continue
    }
    if ($isOurLink) { $existing.Delete() }
    elseif ($isOurCopy) { Remove-Item $dest -Recurse -Force }

    if ($Copy) {
        Copy-Item $src.FullName $dest -Recurse
        New-Item -ItemType File (Join-Path $dest '.oleander') | Out-Null
        Write-Host "copied   $($src.Name)"
    } else {
        New-Item -ItemType Junction -Path $dest -Target $src.FullName | Out-Null
        Write-Host "linked   $($src.Name)"
    }
}
