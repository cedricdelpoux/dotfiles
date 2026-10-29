#!/bin/bash

# Exit if a command fail
set -e

# Command line developer tools
if ! type "gcc" > /dev/null; then
  gcc
fi

# Constants
declare -r ROOT=$(cd $(dirname ${BASH_SOURCE[0]}) && pwd)

# Functions: also available to the overlay (see README)
symlink() {
  local source="$1"
  local target="$HOME/$2"
  [[ "$source" != /* ]] && source="$ROOT/$source"

  echo "Symlink: $target -> $source"
  ln -sfn "$source" "$target"
}

symlink_skills() {
  mkdir -p "$HOME/.claude/skills"
  for skill in "$1"/*/; do
    skill="${skill%/}"
    symlink "$skill" ".claude/skills/$(basename "$skill")"
  done
}

# Scripts: DOTFILES_LINKS_ONLY=1 refreshes the symlinks without brew and macOS setup
if [ -z "$DOTFILES_LINKS_ONLY" ]; then
  source "$ROOT/scripts/brewfile.sh"
  source "$ROOT/scripts/osx.sh"
  source "$ROOT/scripts/shell.sh"
fi

# Symlinks
symlink "git/.gitconfig" ".gitconfig"
symlink "git/.gitexcludes" ".gitexcludes"
symlink "shell/.bash_profile" ".bash_profile"
symlink "shell/.inputrc" ".inputrc"
symlink "shell/.zshrc" ".zshrc"
symlink_skills "$ROOT/skills"

# Overlay: a sibling repo adding its own packages, *.local files and skills
if [ -n "$DOTFILES_OVERLAY" ]; then
  source "$DOTFILES_OVERLAY/overlay.sh"
fi
