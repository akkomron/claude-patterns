#!/usr/bin/env bash
# Link this repo's global Claude Code config into ~/.claude, so every project on this computer follows PATTERN.md.
#
#   git clone <this repo> ~/Projects/claude-patterns && bash ~/Projects/claude-patterns/install.sh
#
# Symlinks, not copies: a `git pull` here updates every machine's config. An existing file that is not already our link
# is moved aside to <name>.bak-<date>, never deleted.
set -euo pipefail
REPO="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/.claude"
mkdir -p "$DEST/skills"

link() {   # link <file in repo> <name in ~/.claude>
  local src="$REPO/$1" dst="$DEST/$2"
  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    echo "ok       $dst"
    return
  fi
  if [ -L "$dst" ] && [[ "$(readlink "$dst")" == "$REPO"/* ]]; then
    rm "$dst"                                  # our own link from an older layout of this repo: only the link goes
  fi
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    mv "$dst" "$dst.bak-$(date +%Y%m%d-%H%M%S)"
    echo "backed up the old $dst"
  fi
  ln -s "$src" "$dst"
  echo "linked   $dst -> $src"
}

link global/CLAUDE.md CLAUDE.md
link skills/ai-project-patterns/PATTERN.md PATTERN.md
link skills/ai-project-patterns skills/ai-project-patterns    # the skill, for machines without the plugin
