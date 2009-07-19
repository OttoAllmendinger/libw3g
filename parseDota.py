import psyco
psyco.full()

from ReplayReader import ReplayReader

from tools import *


def DotaTrigger(block, fp):
    drx = extract_string(fp)
    a = extract_string(fp)
    b = extract_string(fp)
    c = extract(fp, 'L')
    #print locals()

def parseDotaReplay(fp):
    reader = ReplayReader()
    abr = reader.gameBlockReader.actionBlockReader
    abr.define(0x6B, 'DotaTrigger', DotaTrigger)
    reader.parse(fp)



def usage(name):
    print "Usage: %s REPLAY-FILE" % name



if __name__=="__main__":
    import sys
    if len(sys.argv)>1:
        f = sys.argv[1]
        parseDotaReplay(file(f))
    else:
        usage(sys.argv[0])

