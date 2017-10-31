#!/usr/bin/env python
#
# colorize.py
# Fritz Reese
#
# Simple sed-like script to filter terminal color escapes into any text stream.
#

def tdbg(msg):
    import threading
    me = threading.current_thread().name
    sys.stdout.write('[%s] %s\n' % (me, msg))

import select
import signal
import sys
import re
from StringIO import StringIO

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

def usage(errstr=""):
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
    -i	interactive mode: do not line-buffer the input

{colorspecs}:
    -r	{r}		-R	{br}		-k	{k}
    -g	{g}		-G	{bg}		-K	{bk}
    -b	{b}		-B	{bb}		-w	{w}
    -c	{c}		-C	{bc}		-W	{bw}
    -y	{y}		-Y	{by}		-u	{u}
    -m	{m}		-M	{bm}
""".format(**fmt))
    if errstr:
        sys.stderr.write('\n%s\n' % (errstr,))
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

def sigpipe(*args):
    """Called when SIGPIPE is received."""
    sys.stdout.flush ()
    sys.stdout.close ()
    sys.exit (0)

_libc = None
_sched_yield = None
def sched_yield(timeout=0.010):
    """Reliable wrapper around sched_yield() from libc which falls-back to
    time.sleep(timeout) if sched_yield cannot be found from libc.so.6.
    Note the timeout argument is only relevant the first time this wrapper
    is called, as it binds the timeout to the function on load for speed."""
    global _sched_yield
    global _libc
    if _sched_yield is None:
        try:
            import ctypes
            if _libc is None:
                _libc = ctypes.CDLL('libc.so.6')
            _sched_yield = _libc.sched_yield
        except OSError:
            import time
            _sched_yield = lambda : time.sleep(timeout)
    return _sched_yield()

class unbuffered_stream(object):
    def __init__(self, istream):
        self.infd = istream.fileno()
        self.mask = select.POLLIN|select.POLLHUP|select.POLLNVAL|select.POLLERR
        self.poller = select.poll()
        self.poller.register(self.infd, self.mask)
        self.istream = istream
        self.closed = False

    def _get_chars(self):
        """Return all characters available on the input stream at this moment.
        Basically polls the input repeatedly, reading one character at a time
        until the input runs out of characters.
        If no characters are available right now, return the empty string.
        If the stream is closed or encountered an error, return None."""
        if self.closed:
            return None

        # When we _first_ check for characters, it is okay to wait for some to
        # appear. It is only once a set of characters appear on the input that
        # we want to eat them all with no timeout and return them.
        line = StringIO()
        check_list = self.poller.poll(1)
        while check_list and not self.closed:
            # The poller should have at most one element for istream.
            fd, event = check_list[0]
            # assert(fd == self.infd)

            # Collect characters into the line one-by-one.
            # See if we have any more characters for next time.
            if event & select.POLLIN != 0:
                line.write(self.istream.read(1))
                check_list = self.poller.poll(0)

            # For any other event, the stream must be dead.
            elif event != 0:
                self.closed = True

        # Return any characters we have found so far.
        # Even if we are done, we should return any characters we read
        # this time, then return None next time (remembered by self.closed).
        if line:
            ret = line.getvalue()
            line.close()
            return ret

        # Once we are done, if we have no input, return None.
        if self.closed:
            return None

        # If we got no input but still aren't done, just return empty string.
        return ''

    def __iter__(self):
        """Return an iterator yielding a sequence of unbuffered input
        characters roughly as they become available on the input stream.  The
        stream must support the fileno() operation and polling, and the output
        order is subject to CPU scheduling. The colorizing might be off if a
        pattern would require matching characters which end up split between
        two items. This is mostly for small, simple patterns in an interactive
        program (such as highlighting the prompt in an interactive Python
        session).
        """
        # Get available input characters in chunks.  Whence line is None, the
        # stream has been shutdown or experienced an error
        line = self._get_chars()
        while line is not None:
            # Yield non-empty sequences.
            # Empty sequences may appear when the stream has nothing for us yet
            # but we greedily checked anyway.
            if line:
                yield line
            # Don't eat the CPU spinning on empty input.
            sched_yield()
            line = self._get_chars()

def select_lines(istream):
    """Return an iterator yielding a sequence of [line-buffered] input lines.
    Note if the input never ends with a new-line, it will never be yielded."""
    line = istream.readline()
    if line:
        yield line

# each color gets an optional regex argument
_sopts = 'hi'+'::'.join(_kcolors)+'::'

def parse_args(args=None):
    """Parse the arguments according to our usage and return (opts, args)
    as getopt would. If args is not given, use sys.argv[1:] by default."""
    if args is None:
        args = sys.argv[1:]
    from getopt import getopt
    return getopt(args, _sopts)

def colorize(opts, istream=None, ostream=None):
    if istream is None:
        istream = sys.stdin
    if ostream is None:
        ostream = sys.stdout

    # list of ColorMatch objects
    results = list()
    line_iter = select_lines
    for opt, optarg in opts:
        if opt[1] in _kcolors and opt[1].isalpha():
            rx = re.compile (optarg)
            if rx:
                results.append (ColorMatch(rx, opt[1]))
            else:
                usage("bad regex: '%s'" % (optarg,))
        elif opt[1] == 'h':
            usage()
        # Interactive mode - use unbuffered (non-blocking) reads
        elif opt[1] == 'i':
            line_iter = unbuffered_stream

    # copy input to output, filtering colors along the way
    for line in line_iter(istream):
        for cmatch in results:
            line = cmatch.filter(line)

        ostream.write(line)
        ostream.flush ()

    return 0

def main():
    # catch SIGPIPE and close nicely
    signal.signal (signal.SIGPIPE, sigpipe)
    return colorize(parse_args()[0])

if __name__ == '__main__':
    sys.exit (main())
