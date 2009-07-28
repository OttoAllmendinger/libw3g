import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

try:
    from betterprint import pprint
except ImportError:
    from pprint import pprint


import parseDota



def dumpState(gamestate):
    pprint(gamestate)

def dumpSlots(state):
    print state['DotA']['ModeLine']
    for s in state['Slots'].values():
        stats = s['Stats']
        #print '%-25s: %-25s' % (s['Name'], stats['Hero'])
        kills, deaths, assists = stats.get('Kills'), stats.get('Deaths'), stats.get('Assists')
        #pprint(stats)
        print '%-24s | %-48s | %s/%s/%s' % (s['Name'], stats['Hero'], kills, deaths, assists)

def usage(name):
    print "Usage: %s REPLAY-FILE" % name



if __name__=="__main__":
    import sys
    for arg in sys.argv[1:]:
        if arg=='-d':
            basicConfig(level=1)
        else:
            state = parseDota.parseDotaReplay(file(arg))

        #dumpState(state)
        dumpSlots(state)

    if len(sys.argv)==1:
        usage(sys.argv[0])

