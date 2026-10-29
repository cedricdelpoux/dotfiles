# List
alias l="ls -la"       # All files, include dotfiles
alias ld="ls -ld */"   # Directories

# Cd
alias ..="cd .."
alias ...="cd ../.."
alias ....="cd ../../.."

# Terminal
alias copypath="pwd|pbcopy"

# GPG
export GPG_TTY=$(tty)

# Machine-specific additions (installed by an overlay, see README)
[ -f "$HOME/.bash_profile.local" ] && source "$HOME/.bash_profile.local"
