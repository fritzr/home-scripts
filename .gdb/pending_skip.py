import gdb

to_skip = []

def try_pending_skips(evt=None):
    for skip in list(to_skip): # make a copy for safe remove
        skipargs = skip.split()
        print 'loading skip: ' + skip
        # If it is a function, make sure the symbol is defined
        if len(skipargs) < 1 or skipargs[0] == 'function':
            try:
                # test if the function (aka symbol is defined)
                symb, _ = gdb.lookup_symbol(skip)
                if not symb:
                    continue
            except gdb.error:
                # no frame ?
                continue
            # yes, we can skip it
            gdb.execute("skip " + str(skip))
            to_skip.remove(skip)
        # otherwise who knows what is happening

    if not to_skip:
        # no more functions to skip
        try:
            gdb.events.new_objfile.disconnect(try_pending_skips) # event fired when the binary is loaded
        except (gdb.error, ValueError):
            pass # was not connected

class cmd_pending_skip(gdb.Command):
    self = None

    def __init__ (self):
        gdb.Command.__init__(self, "pending_skip", gdb.COMMAND_OBSCURE)

    def invoke (self, args, from_tty):
        global to_skip

        if not args:
            if not to_skip:
                print("No pending skip.")
            else:
                print("Pending skips:")
                for skip in to_skip:
                    print("\t" + str(skip))
            return

        skip = args
        to_skip.append(skip)

        print("Pending skip for '%s' registered."%(skip,))

        # for some reason this really pisses GDB off
        #try:
        #    gdb.events.new_objfile.disconnect(try_pending_skips)
        #except: pass # was not connected

        # new_objfile event fired when the binary and libraries are loaded in memory
        gdb.events.new_objfile.connect(try_pending_skips)

        # try right away, just in case
        #try_pending_skips()

cmd_pending_skip()
