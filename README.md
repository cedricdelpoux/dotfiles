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

After a `git pull` of this repo or the overlay, refresh the symlinks (dotfiles, Claude skills, Claude
scripts, VS Code extension) without the Homebrew and macOS setup:

```
DOTFILES_LINKS_ONLY=1 ~/Code/dotfiles-<machine>/install.sh
```

## Writing an overlay

- `DOTFILES_OVERLAY=<repo> ./install.sh` sources `<repo>/overlay.sh` at the end, with `symlink`,
  `symlink_skills`, `install` and `install_cask` available.
- `~/.zshrc.local`, `~/.bash_profile.local` and `~/.gitconfig.local` are sourced/included when
  present: the overlay symlinks its own versions there (git identity goes in `.gitconfig.local`).
- Claude skills: `skills/<name>/SKILL.md` here and in the overlay are symlinked into `~/.claude/skills/`.

## VS Code integrated browser

`claude/bin/vscode-browser <file or URL>` opens a page in the VS Code integrated browser and reuses
the tab already on it. It goes through `vscode/browser-open`, a local extension whose URI handler
runs `workbench.action.browser.open`. A local file must be inside a trusted workspace folder.
After the symlinks are created, run Developer: Reload Window in VS Code so it loads the extension.
If the command opens nothing, the extension is not loaded: check
`~/.vscode/extensions/local.browser-open-0.0.1`, then reload the window.

