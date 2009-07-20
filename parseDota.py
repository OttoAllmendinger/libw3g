import psyco
psyco.full()

import time

from ReplayReader import ReplayReader
from ActionBlockReader import ActionBlockReader

from Tools import *

from logging import basicConfig

import json

from pprint import pprint



class DotaActionBlockReader(ActionBlockReader):
    def __init__(self, gamestate):
        ActionBlockReader.__init__(self, gamestate)
        self.define(0x6B, 'DotaTrigger')

    def handleDotaTrigger(self, block, io):
        drx = extractString(io)
        a = extractString(io)
        b = extractString(io)
        c = extract('L', io)
        self.state['Dota-Events'].append((a,b,c))

def parseDotaReplay(io):
    gamestate = {
            'Parse-Time': time.asctime(),
            'Game-Time': 0,
            'Dota-Events': []
    }

    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    reader.parse(io)

    return gamestate


def output(gamestate):
    #print json.dumps(gamestate)
    pprint(gamestate)

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

