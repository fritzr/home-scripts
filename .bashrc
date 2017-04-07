# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

# Like '[\u@\h \W]$ ' but with the '\u@\h' bolded and '\W' underlined
export PS1='[\[\e[1m\]\u@\h\[\e[0m\] \[\e[4m\]\W\[\e[0m\]]$ '
eval $(dircolors -b $HOME/.dircolors)

# Machine-specific definitions
if [ -f /data/.bashrc ]; then
  . /data/.bashrc
else
  PATH_DEFAULT="$HOME/bin"
fi

# Create local config files so various applications don't complain about them
test -f "$HOME/.vimrc.local" || touch "$HOME/.vimrc.local"
test -f "$HOME/.gdb.local" || touch "$HOME/.vimrc.local"
test -f "$HOME/.gitconfig.local" || touch "$HOME/.vimrc.local"

# used by ~/.vim/plugin/gnuchlog.vim and git
export EMAIL="fritzoreese@gmail.com"
export EDITOR="/usr/bin/vim"

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

# cross-compiled toolchains
XSUPPORT="/data/x-tools/device-support"
XTOOLS="/data/x-tools/cent65/gcc63"
XARM="$XTOOLS/arm-eabi-linux-gnueabi"
  XARM_SUP="$XARM/device-support"
  XARM_BIN="$XARM/bin"
  XARM_LIB="$XARM/lib64:$XARM/lib"
XX86="$XTOOLS/x86_64-eabi-linux-gnu"
  XX86_SUP="$XX86/device-support"
  XX86_BIN="$XX86/bin"
  XX86_LIB="$XX86/lib64:$XX86/lib:$XX86_SUP/lib64:$XX86_SUP/lib"
XARM64="$XTOOLS/aarch64-eabi-linux-gnueabi"
  XARM64_SUP="$XARM64/device-support"
  XARM64_BIN="$XARM64/bin"
  XARM64_LIB="$XARM64/lib64:$XARM64/lib:$XARM64_SUP/lib64:$XARM64_SUP/lib"
XPATH="$XARM_BIN:$XX86_BIN" # :$XARM64
XLDPATH="$XARM_LIB:$XX86_LIB"

# xt arm|x86|arm64
function xt() {
  case $1 in
    [aA][rR][mM]) false ;;
    [aA][rR][mM]64) false ;;
    [xX]86) false ;;
  esac
  if [ $? != 0 ]; then
    _tool=$(echo $1 | tr [a-z] [A-Z])
    _xdir=$(eval echo \$X${_tool})
    _xbin=$(eval echo \$X${_tool}_BIN)
    _xlib=$(eval echo \$X${_tool}_LIB)
    echo xtools: using $(basename $(eval echo \$X${_tool}))
    export LD=${_xbin}/*-ld
    export CC=${_xbin}/*-gcc
    export CXX=${_xbin}/*-g++
    export CFLAGS="-I${_xdir}/include -I${_xdir}/device-support/include"
    export LDFLAGS="-L$(echo $_xlib | sed 's/:/ -L/g')"
    export STRIP=${_xbin}/*-strip
    export PATH="$_xbin:$PATH_DEFAULT"
    export LD_LIBRARY_PATH="$_xlib:$LD_LIBRARY_PATH_DEFAULT"
    export HOST=$(basename $_xdir)
  else
    echo xtools: cleared
    export LD=
    export CC=
    export CXX=
    export CFLAGS=
    export LDFLAGS=
    export STRIP=
    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH_DEFAULT"
    export PATH="$PATH_DEFAULT"
    export HOST=
  fi
}

ZDBIN="$ZD/src/bin:$ZD/utils/bin:$ZD/fwdb/bin:$ZD/fwdb/vendor/bin:$ZD/src/bin/host"
ZDSCR="$ZD/src/scripts:$ZD/utils/scripts"
LIB_LOCAL="$HOME/.local/lib64:$HOME/.local/lib"

HEIMDALL="$WZD/opensrc/Heimdall/bin"
# adb on sulabmbb
ADB_PATH=""
if [ -x /data/adb ]; then
  ADB_PATH=":/data"
fi

export IDAPATH="/opt/ida-6.5"
if [ ! -d "$IDAPATH" ]; then
  export IDAPATH=""
fi

PATH_DEFAULT="$PATH_DEFAULT:$ZDSCR:$ZDBIN"
PATH_DEFAULT="$PATH_DEFAULT:$DATA/xpwn/ipsw-patch:$IDAPATH"
PATH_DEFAULT="$PATH_DEFAULT:/usr/lib64/qt-3.3/bin:$INTEL_PATH"
PATH_DEFAULT="$PATH_DEFAULT:/usr/bin:$OSRC$ADB_PATH"
export PATH_DEFAULT="$PATH_DEFAULT:/usr/local/bin:/usr/bin:/bin"
LD_GCC_PATH="$DATA/support/lib:$DATA/support/lib32:$MYGDB/lib"
LD_LIBRARY_PATH_DEFAULT="$LD_GCC_PATH:$LIB_LOCAL"

MANPATH_DEFAULT="$MANPATH_DEFAULT:/usr/share/man:$HOME/share/man"
MANPATH_DEFAULT="$MANPATH_DEFAULT:$HOME/.local/share/man"
export MANPATH_DEFAULT
export LD_LIBRARY_PATH_DEFAULT

export PATH="$PATH_DEFAULT"
export MANPATH="$MANPATH_DEFAULT"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH_DEFAULT"

alias mysqld="nohup mysqld_safe \
--port=3307 \
--pid-file=$MSQLD/mysql.pid \
--socket=$MSQLD/mysql.sock \
--log-error=$MSQLD/err.log \
--datadir=$MSQLD/data | tee $MSQLD/startup.log &"
alias mysql="/usr/bin/mysql --socket=$MSQLD/mysql.sock"
alias mysqladmin="/usr/bin/mysqladmin --socket=$MSQLD/mysql.sock"

function search() { grep -rIs "$@" . ; }
function calc() { python -c "print(eval('$*'))" ; }

HOST=$(hostname | cut -d. -f1)
function wd() { pwd | sed "s=$HOME=~=" ; }
function pts() { tty | cut -d/ -f4 ; }
PROMPT_COMMAND='echo -en "\033]0;[tty-$(pts)] $(whoami)@$HOST:$(wd)\a"'
