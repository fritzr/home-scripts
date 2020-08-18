# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

# Local definitions.
PATH=/usr/bin:/bin:/usr/sbin:/sbin
LD_LIBRARY_PATH=
MANPATH=
PYTHONPATH=

# Initialize the rcfile system and source rcfiles.
if [[ -d ~/.bashrc.d ]]; then
  : ${RCDIR:=~/.bashrc.d}
  export RCDIR
  _rcinit="$(find ~/.bashrc.d -name bashrc -print -quit 2>/dev/null)"
  if [[ -f "${_rcinit}" ]]; then
    # setup rcfiles_source function.
    . "${_rcinit}"
  fi
  if type -p rcfiles_source; then
    rcfiles_source
  fi
fi
