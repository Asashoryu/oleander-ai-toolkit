#!/usr/bin/env bash
# Installs oleander skills and workflows into the Claude Code skills directory.
# Default: creates symlinks, so edits in this repo are live.
# Also lists what it installed in the matching CLAUDE.md (~/.claude/CLAUDE.md or <project>/CLAUDE.md).
#   --copy        copy folders instead of linking
#   --uninstall   remove only entries that this repo installed
#   --update      pull the latest changes from the repository, then install
#   --target DIR  install directory (default: ~/.claude/skills)
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
target="$HOME/.claude/skills"
mode=link
update=0
args=()

while [ $# -gt 0 ]; do
    case "$1" in
        --update) update=1; shift; continue ;;
        --copy) mode=copy; args+=("$1") ;;
        --uninstall) mode=uninstall; args+=("$1") ;;
        --target) target="$2"; args+=("$1" "$2"); shift ;;
        -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
        *) echo "unknown option: $1" >&2; exit 1 ;;
    esac
    shift
done

if [ "$update" = 1 ]; then
    [ "$mode" = uninstall ] && { echo "--update cannot be combined with --uninstall" >&2; exit 1; }
    git -C "$repo" pull --ff-only
    exec "$repo/setup.sh" "${args[@]}"   # rerun the freshly pulled script
fi

sources=()
for dir in "$repo"/skills/*/ "$repo"/workflows/*/; do
    [ -f "$dir/SKILL.md" ] && sources+=("${dir%/}")
done

dupes="$(for s in "${sources[@]}"; do basename "$s"; done | sort | uniq -d)"
if [ -n "$dupes" ]; then
    echo "Duplicate names across skills/ and workflows/: $dupes" >&2
    exit 1
fi

mkdir -p "$target"
installed=()

for src in "${sources[@]}"; do
    name="$(basename "$src")"
    dest="$target/$name"
    ours=""
    if [ -L "$dest" ] && [ "$(readlink -f "$dest")" = "$(readlink -f "$src")" ]; then
        ours=link
    elif [ -d "$dest" ] && [ ! -L "$dest" ] && [ -f "$dest/.oleander" ]; then
        ours=copy
    fi

    if [ "$mode" = uninstall ]; then
        [ -n "$ours" ] && rm -rf "$dest" && echo "removed  $name"
        continue
    fi

    if [ -e "$dest" ] || [ -L "$dest" ]; then
        if [ -z "$ours" ]; then
            echo "warning: skip $name: $dest exists and was not installed by this repo" >&2
            continue
        fi
        rm -rf "$dest"
    fi

    if [ "$mode" = copy ]; then
        cp -r "$src" "$dest"
        touch "$dest/.oleander"
        echo "copied   $name"
    else
        ln -s "$src" "$dest"
        echo "linked   $name"
    fi
    installed+=("$src")
done

# CLAUDE.md that loads alongside the target: ~/.claude/CLAUDE.md, or <project>/CLAUDE.md for <project>/.claude/skills
parent="$(cd "$target/.." && pwd)"
if [ "$parent" = "$(cd "$HOME" && pwd)/.claude" ]; then
    claude_md="$parent/CLAUDE.md"
elif [ "$(basename "$parent")" = .claude ]; then
    claude_md="$(dirname "$parent")/CLAUDE.md"
else
    echo "warning: $target is not a .claude/skills folder, CLAUDE.md not updated" >&2
    exit 0
fi

start='<!-- oleander-ai-toolkit:start -->'
end='<!-- oleander-ai-toolkit:end -->'
rest=""
if [ -f "$claude_md" ]; then
    # drop the previous block and trailing blank lines
    rest="$(awk -v s="$start" -v e="$end" '
        $0 == s { skip = 1 }
        !skip   { line[++n] = $0 }
        $0 == e { skip = 0 }
        END     { while (n > 0 && line[n] ~ /^[[:space:]]*$/) n--; for (i = 1; i <= n; i++) print line[i] }
    ' "$claude_md")"
fi

if [ "$mode" = uninstall ] || [ ${#installed[@]} -eq 0 ]; then
    if [ -f "$claude_md" ]; then
        if [ -n "$rest" ]; then printf '%s\n' "$rest" > "$claude_md"; else rm "$claude_md"; fi
        echo "updated  $claude_md"
    fi
    exit 0
fi

{
    if [ -n "$rest" ]; then printf '%s\n\n' "$rest"; fi
    echo "$start"
    echo "## oleander-ai-toolkit"
    echo
    echo "Installed from \`$repo\`. Workflows run only when the user types their slash command: when a request fits one, suggest it."
    echo
    for src in "${installed[@]}"; do
        name="$(basename "$src")"
        desc="$(sed -n 's/^description: *//p' "$src/SKILL.md" | head -n1)"
        case "$src" in
            */workflows/*) echo "- \`/$name\` (workflow): ${desc#Workflow: }" ;;
            *) echo "- \`$name\` (skill): $desc" ;;
        esac
    done
    echo "$end"
} > "$claude_md"
echo "updated  $claude_md"
