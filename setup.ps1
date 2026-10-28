<#
.SYNOPSIS
  Installs oleander skills and workflows into the Claude Code skills directory.
.DESCRIPTION
  Default: creates directory junctions (no admin needed), so edits in this repo are live.
  Also lists what it installed in the matching CLAUDE.md (~/.claude/CLAUDE.md or <project>/CLAUDE.md).
  -Copy      copy folders instead of linking
  -Uninstall remove only entries that this repo installed
  -Update    pull the latest changes from the repository, then install
  -Target    install directory (default: ~/.claude/skills)
#>
param(
    [switch]$Copy,
    [switch]$Uninstall,
    [switch]$Update,
    [string]$Target = (Join-Path $HOME '.claude\skills')
)

$ErrorActionPreference = 'Stop'

if ($Update) {
    if ($Uninstall) { throw '-Update cannot be combined with -Uninstall' }
    git -C $PSScriptRoot pull --ff-only
    if ($LASTEXITCODE -ne 0) { throw 'git pull failed' }
    & $PSCommandPath -Copy:$Copy -Target $Target   # rerun the freshly pulled script
    return
}
$sources = @('skills', 'workflows') |
    ForEach-Object { Join-Path $PSScriptRoot $_ } |
    Where-Object { Test-Path $_ } |
    ForEach-Object { Get-ChildItem $_ -Directory } |
    Where-Object { Test-Path (Join-Path $_.FullName 'SKILL.md') }

$dupes = $sources | Group-Object Name | Where-Object Count -gt 1
if ($dupes) { throw "Duplicate names across skills/ and workflows/: $($dupes.Name -join ', ')" }

New-Item -ItemType Directory -Force $Target | Out-Null
$installed = @()

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
    $installed += $src
}

# CLAUDE.md that loads alongside the target: ~/.claude/CLAUDE.md, or <project>/CLAUDE.md for <project>/.claude/skills
$parent = (Resolve-Path (Join-Path $Target '..')).Path.TrimEnd('\')
if ($parent -eq (Join-Path $HOME '.claude')) { $claudeMd = Join-Path $parent 'CLAUDE.md' }
elseif ((Split-Path $parent -Leaf) -eq '.claude') { $claudeMd = Join-Path (Split-Path $parent) 'CLAUDE.md' }
else { Write-Warning "$Target is not a .claude\skills folder, CLAUDE.md not updated"; return }

$start = '<!-- oleander-ai-toolkit:start -->'
$end = '<!-- oleander-ai-toolkit:end -->'
$utf8 = New-Object System.Text.UTF8Encoding $false
$rest = ''
if (Test-Path $claudeMd) {
    $old = [IO.File]::ReadAllText($claudeMd)
    $pattern = '(?s)' + [regex]::Escape($start) + '.*?' + [regex]::Escape($end)
    $rest = ([regex]::Replace($old, $pattern, '')).TrimEnd()
}

if ($Uninstall -or $installed.Count -eq 0) {
    if (Test-Path $claudeMd) {
        if ($rest) { [IO.File]::WriteAllText($claudeMd, "$rest`n", $utf8) } else { Remove-Item $claudeMd }
        Write-Host "updated  $claudeMd"
    }
    return
}

$lines = @($start, '## oleander-ai-toolkit', '',
    "Installed from ``$PSScriptRoot``. Workflows run only when the user types their slash command: when a request fits one, suggest it.", '')
foreach ($src in $installed) {
    $desc = (Select-String -Path (Join-Path $src.FullName 'SKILL.md') -Pattern '^description:\s*(.*)' | Select-Object -First 1).Matches.Groups[1].Value
    if ($src.Parent.Name -eq 'workflows') { $lines += "- ``/$($src.Name)`` (workflow): $($desc -replace '^Workflow:\s*', '')" }
    else { $lines += "- ``$($src.Name)`` (skill): $desc" }
}
$lines += $end
$block = $lines -join "`n"
$text = if ($rest) { "$rest`n`n$block`n" } else { "$block`n" }
[IO.File]::WriteAllText($claudeMd, $text, $utf8)
Write-Host "updated  $claudeMd"
