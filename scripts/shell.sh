if [ ! -e "$HOME/.zshrc" ]; then
  echo "Zsh: install"
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

  echo "Zsh: Set as default shell"
  chsh -s /bin/zsh
fi
