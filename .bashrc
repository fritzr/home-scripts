# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

# Local definitions.
export PATH=/usr/bin:/bin:/usr/sbin:/sbin
export LD_LIBRARY_PATH=
export MANPATH=
export PYTHONPATH=

if [[ -d ~/.bashrc.d ]]; then
  # Initialize the rcfile system and source rcfiles.
  export RCDIR=~/.bashrc.d
  _rcinit="$(/usr/bin/find ~/.bashrc.d -name bashrc -print -quit 2>/dev/null)"
  if [[ -e "${_rcinit}" ]]; then
    . "${_rcinit}"
  fi
  if type -p rcfiles_source; then
    # Use unity rcfile unless env specifies not to
    if [[ -z "${NO_BASHRC_UNITY}" ]]; then
      rcfiles_source -u
    else
      rcfiles_source -f
    fi
  fi
fi
