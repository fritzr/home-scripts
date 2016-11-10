#!/usr/bin/env python
#
# colorize.py
# Fritz Reese
#
# Simple sed-like script to filter terminal color escapes into any text stream.
#

import sys
import re
from StringIO import StringIO
from getopt import getopt

_RESET = "\033[0m"
_UNDER    = "\033[4m"
_BLACK    = "\033[30m"
_RED      = "\033[31m"
_GREEN    = "\033[32m"
_YELLOW   = "\033[33m"
_BLUE     = "\033[34m"
_MAGENTA  = "\033[35m"
_CYAN     = "\033[36m"
_WHITE    = "\033[37m"
_BBLACK   = "\033[1m\033[30m"
_BRED     = "\033[1m\033[31m"
_BGREEN   = "\033[1m\033[32m"
_BYELLOW  = "\033[1m\033[33m"
_BBLUE    = "\033[1m\033[34m"
_BMAGENTA = "\033[1m\033[35m"
_BCYAN    = "\033[1m\033[36m"
_BWHITE   = "\033[1m\033[37m"

_colors = {
  'u' : _UNDER,    # underline
  'k' : _BLACK,    # Black
  'r' : _RED,      # Red
  'g' : _GREEN,    # Green
  'y' : _YELLOW,   # Yellow
  'b' : _BLUE,     # Blue
  'm' : _MAGENTA,  # Magenta
  'c' : _CYAN,     # Cyan
  'w' : _WHITE,    # White
  'K' : _BBLACK,   # Bold Black
  'R' : _BRED,     # Bold Red
  'G' : _BGREEN,   # Bold Green
  'Y' : _BYELLOW,  # Bold Yellow
  'B' : _BBLUE,    # Bold Blue
  'M' : _BMAGENTA, # Bold Magenta
  'C' : _BCYAN,    # Bold Cyan
  'W' : _BWHITE,   # Bold White
}

_names = {
  'u' : 'underline',
  'k' : 'black',    # Black
  'r' : 'red',      # Red
  'g' : 'green',    # Green
  'y' : 'yellow',   # Yellow
  'b' : 'blue',     # Blue
  'm' : 'magenta',  # Magenta
  'c' : 'cyan',     # Cyan
  'w' : 'white',    # White
  'K' : 'bold black',   # Bold Black
  'R' : 'bold red',     # Bold Red
  'G' : 'bold green',   # Bold Green
  'Y' : 'bold yellow',  # Bold Yellow
  'B' : 'bold blue',    # Bold Blue
  'M' : 'bold magenta', # Bold Magenta
  'C' : 'bold cyan',    # Bold Cyan
  'W' : 'bold white',   # Bold White
}

_kcolors = 'rgbcymkwRGBCYMKWu'

def usage():
  fmt = dict()
  for k in _kcolors:
    key = k
    if k.isupper():
      key = 'b'+k.lower()
    fmt[key] = _colors[k]+_names[k]+_RESET

  fmt['prog']       = _RED   + sys.argv[0]  + _RESET
  fmt['options']    = _GREEN + 'OPTIONS'    + _RESET
  fmt['colorspecs'] = _CYAN  + 'COLORSPECS' + _RESET
  fmt['flags']      = _UNDER + _kcolors     + _RESET

  sys.stderr.write("""
Usage: {prog} [{options}] [{colorspecs}...]
Apply color filters to the input according to the {colorspecs}.
Each COLORSPEC is one of [-{flags}] followed by an optional REGEX.

Where the regex is matched in the input it will be colored the corresponding
color. If the regex has a match group (parenthesis), only the [first] group
will be colorized.

{options}:
  none yet

{colorspecs}:
  -r	{r}		-R	{br}		-k	{k}
  -g	{g}		-G	{bg}		-K	{bk}
  -b	{b}		-B	{bb}		-w	{w}
  -c	{c}		-C	{bc}		-W	{bw}
  -y	{y}		-Y	{by}		-u	{u}
  -m	{m}		-M	{bm}
""".format(**fmt))
  sys.stderr.flush()
  sys.exit(1)

class ColorMatch(object):
  def __init__(self, rx, colorkey):
    self.rx = rx
    self.ck = colorkey
    self.ct = _colors[colorkey]

  def filter(self, text):
    """Filter a string, adding this object's color to all instances where
    this object matches text in the string."""
    off = 0
    out = StringIO()
    for m in self.rx.finditer(text):
      # Insert the color escapes before and after the matched portion.
      # This is verbose but more efficient than regular concatenation.
      if not m.group():
        continue
      out.write(text[off:m.start()])
      out.write(self.ct)
      out.write(m.group())
      out.write(_RESET)
      off = m.end()
    out.write(text[off:])
    ret = out.getvalue()
    out.close()
    return ret

  def __str__(self):
    return _names[self.ck]

def main():
  # list of ColorMatch objects
  results = list()

  # each color gets an optional regex argument
  opts, args = getopt(sys.argv[1:], 'h'+('::'.join(_kcolors)+'::'))

  for opt, optarg in opts:
    if opt[1] in _kcolors and opt[1].isalpha():
      rx = re.compile (optarg)
      if rx:
        results.append (ColorMatch(rx, opt[1]))
      else:
        sys.stderr.write('bad regex %s\n' % (optarg))
    elif opt[1] == 'h':
      usage()

  ret = 0
  if len(args) > 0:
    ret = int(args[0])

  # copy input to output, filtering colors along the way
  while True:
    line = sys.stdin.readline ()
    if not line:
      break

    for cmatch in results:
      line = cmatch.filter(line)

    sys.stdout.write(line)

  return ret

if __name__ == '__main__':
  sys.exit (main())
