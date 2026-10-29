# dotfiles

The setup every machine shares: shell, git, macOS defaults, the base Homebrew packages and the Claude
Code skills. Nothing machine-specific lives here: an overlay repo adds it.

| Machine | Overlay |
|---|---|
| personal | [dotfiles-perso](https://github.com/cedricdelpoux/dotfiles-perso) |
| Veson | [dotfiles-veson](https://github.com/cedricdelpoux/dotfiles-veson) |

Install the overlay, it clones this repo and runs it:

```
git clone git@github.com:cedricdelpoux/dotfiles-<machine> ~/Code/dotfiles-<machine>
~/Code/dotfiles-<machine>/install.sh
```

`DOTFILES_LINKS_ONLY=1 <overlay>/install.sh` refreshes the symlinks (dotfiles, Claude skills) without
the Homebrew and macOS setup, e.g. after a `git pull`.

## Writing an overlay

- `DOTFILES_OVERLAY=<repo> ./install.sh` sources `<repo>/overlay.sh` at the end, with `symlink`,
  `symlink_skills`, `install` and `install_cask` available.
- `~/.zshrc.local`, `~/.bash_profile.local` and `~/.gitconfig.local` are sourced/included when
  present: the overlay symlinks its own versions there (git identity goes in `.gitconfig.local`).
- Claude skills: `skills/<name>/SKILL.md` here and in the overlay are symlinked into `~/.claude/skills/`.
