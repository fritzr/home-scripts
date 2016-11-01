# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

eval $(dircolors -b $HOME/.dircolors)

# Machine-specific definitions
if [ -f /data/.bashrc ]; then
  . /data/.bashrc
fi

# used by ~/.vim/plugin/gnuchlog.vim and git
export NAME="Fritz Reese"
export EMAIL="fritzoreese@gmail.com"
export EDITOR="/usr/bin/vim"

export PATH_DEFAULT="$PATH_DEFAULT:/usr/local/bin:/usr/bin:/bin"
MANPATH_DEFAULT="$MANPATH_DEFAULT:/usr/share/man:$HOME/share/man"
MANPATH_DEFAULT="$MANPATH_DEFAULT:$HOME/.local/share/man"
export MANPATH_DEFAULT
export LD_LIBRARY_PATH_DEFAULT

export PATH="$PATH_DEFAULT"
export MANPATH="$MANPATH_DEFAULT"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH_DEFAULT"

# Set up custom command-line completions
source $HOME/.complete.d/completions

# Reload bashrc
alias reload=". ~/.bashrc"

# Grep in fortran files
alias grepf="grep -rI --include=*.{f,for}"

# Make and notify
alias maken="make; notify"
# Make, install and notify
alias makein="make && notify && make install; notify"

# Convenience
alias g="git"
alias gst="git status -uno"
alias gdf="git diff"
alias gdfc="git diff --cached"
alias glog="git log"
alias gsh="git show"

function hex() {
python -c "print hex($*)"
}
function dec() {
python -c "print int($*)"
}

# Too dangerous a command to be so similar to 'vi'
alias ci="/bin/false"
alias vi=vim

alias lsc="ls --color=none"
function ltr(){
  ls -ltr ${@} | tail
}

# 64MB core size
ulimit -c 67108864
