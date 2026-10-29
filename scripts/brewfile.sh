# Install
if ! type "brew" > /dev/null; then
  echo "Homebrew: install"
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
fi

# Functions: also available to the overlay (see README)
install() {
  if ! brew ls --versions $1 > /dev/null; then
    echo "Homebrew: install $1"
    brew install $1
  fi
}

install_cask() {
  if ! brew info cask & > /dev/null; then
    echo "Homebrew: install app $1"
    brew install --cask $1
  fi
}

# Upgrade
echo "Homebrew: upgrade"
brew upgrade

# Only what every machine needs: the rest belongs to an overlay
install "git"
install "node"
install "zsh"
install_cask "visual-studio-code"
install_cask "font-fira-code"
install_cask "font-meslo-for-powerline"

# Cleanup
echo "Homebrew: cleaning up"
brew cleanup
