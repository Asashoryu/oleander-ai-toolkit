#!/usr/bin/env bash
# Installs oleander skills and workflows into the Claude Code skills directory.
# Default: creates symlinks, so edits in this repo are live.
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
        -h|--help) sed -n '2,7p' "$0"; exit 0 ;;
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
done
