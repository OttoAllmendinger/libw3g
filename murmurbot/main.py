import sys
import Ice

from MurmurBot import MurmurBot

if __name__=="__main__":
    ic = Ice.initialize(sys.argv)
    try:
        MurmurBot(ic).run()
    except:
        print 'destroying ic...'
        ic.destroy()
        raise
