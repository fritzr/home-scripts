
#set confirm off
set verbose on
set history filename ~/.gdb_history
set history save

# SETTING OUTPUT-RADIX CAUSES GDB TO SEGFAULT SOMETIMES
#set output-radix 16
#set input-radix 10

# These make gdb never pause in its output
set height 0
set width 0

# Pretty prints
set print array on
set print pretty on
set print demangle on
set print asm-demangle
set print object on

# sometimes we randomly get sigttou
handle SIGTTOU nopass nostop

source ~/.gdb/gdbinit.py

set $AUTO_LIST = 1

define hook-stop
  if ( $AUTO_LIST )
    listme
  end
end

define hookpost-up
  if ( $AUTO_LIST )
    listme
  end
end

define hookpost-down
  if ( $AUTO_LIST )
    listme
  end
end
