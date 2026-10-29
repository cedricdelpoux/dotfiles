# Yarn
export PATH="$HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH"

# NVM
export NVM_DIR="$HOME/.nvm"
NVM_PATH="$(brew --prefix nvm)"
[ -s "$NVM_PATH/nvm.sh" ] && \. "$NVM_PATH/nvm.sh"  # This loads nvm
[ -s "$NVM_PATH/etc/bash_completion.d/nvm" ] && \. "$NVM_PATH/etc/bash_completion.d/nvm"  # This loads nvm bash_completion

# Brew
BREW_PATH="$(brew --prefix)"

# Theme
ZSH_THEME="agnoster"

plugins=(
  copypath
  dirhistory
  git
  history
  zsh-autosuggestions
  zsh-syntax-highlighting
)

source $HOME/.oh-my-zsh/oh-my-zsh.sh

prompt_context() {}

# Machine-specific additions (installed by an overlay, see README)
[ -f "$HOME/.zshrc.local" ] && source "$HOME/.zshrc.local"
