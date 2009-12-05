import code
import sys
import traceback
import Ice
import Murmur

status, ic = None, 0
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("Meta:tcp -h 127.0.0.1 -p 6502")
    meta = Murmur.MetaPrx.checkedCast(base)
    if not meta:
        raise RuntimeError("Invalid Proxy")
    #code.interact(local=locals())
    server = meta.getAllServers()[0]
    server.sendMessageChannel(0, True, "test")
except:
    traceback.print_exc()
    status = 1


if ic:
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
