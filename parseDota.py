import psyco
psyco.full()

import time
import json

from pprint import pprint
from datetime import timedelta
from logging import basicConfig

from ReplayReader import ReplayReader
from ActionBlockReader import ActionBlockReader
from Tools import *
from Game import *


DEBUG = False


class DotaActionBlockReader(ActionBlockReader):
    def __init__(self, gamestate):
        ActionBlockReader.__init__(self, gamestate)

        self.dotastate = {
                'events': [],
                'modeline': None
        }

        self.state['dota'] = self.dotastate

        self.define(0x6B, 'DotaTrigger')

    def handleChatTrigger(self, block, io):
        extract('LL', io)
        message = extractString(io)

        if self.currentPlayer['isHost'] and\
                self.dotastate['modeline']==None:
            self.dotastate['modeline'] = message

    def handleDotaTrigger(self, block, io):
        drx = extractString(io)
        a = extractString(io)
        b = extractString(io)
        c, = extract('L', io)
        self.dotastate['events'].append((self.state['gametime'], (a,b,c)))


def blockDebug(reader, block, io):
    state = reader.state

    if block.name=='ChatTrigger':
        state['debug']['lastblocktime'] = state['gametime'] + 1000

    if state['gametime']<state['debug'].get('lastblocktime', 0):
        if isinstance(reader, DotaActionBlockReader):
            if block.blockId==0x16:
                print reader.currentPlayer['name']
                dump(io.read(4))
                print

def parseDotaReplay(io):
    gamestate = emptyState()
    gamestate.update({
            'parsetime': time.asctime(),
    })


    if DEBUG:
        gamestate['debug']['blockdebugger'] = blockDebug


    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    #reader.gameBlockReader.debug = DEBUG
    reader.gameBlockReader.actionBlockReader.debug = DEBUG
    reader.parse(io)

    return gamestate


def output(gamestate):
    #print json.dumps(gamestate)
    #pprint(gamestate)

    print "mode: %s" % gamestate['dota']['modeline']
    print "duration: %s" % formatGametime(gamestate['gametime'])

    for p_id, player in gamestate['playerMap'].items():
        dspname = player['name']+(' (Host)' if player['isHost'] else '')
        print 'id=%s race=%s name=%s' % (p_id, player['race'], dspname)

    #pprint(gamestate['playerMap'])

    #for slot in gamestate['startrecord']['slots']:
        #print 'color=%(color)s id=%(id)s race=%(race)s' % slot

    for ts, (a,b,c) in gamestate['dota']['events']:
        if b=='id' or 1:
            print "%s    %-8s %-12s %s" % (formatGametime(ts), a, b, c)


def usage(name):
    print "Usage: %s REPLAY-FILE" % name


if __name__=="__main__":
    import sys
    for arg in sys.argv[1:]:
        if arg=='-d':
            basicConfig(level=1)
        else:
            state = parseDotaReplay(file(arg))
        output(state)
    if len(sys.argv)==1:
        usage(sys.argv[0])

