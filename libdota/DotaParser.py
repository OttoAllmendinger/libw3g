#/usr/bin/python
#coding=utf8

try:
    import psyco
    #psyco.full()
except ImportError:
    print 'install psyco for speedup'

import time

from libw3g.ReplayReader import ReplayReader
from libw3g.ActionBlockReader import ActionBlockReader

from libw3g.Tools import *
from DotaUnits import *


def dotaTime(t):
    return t # TODO: fix timing issues?

class DotaActionBlockReader(ActionBlockReader):
    def __init__(self, gamestate):
        ActionBlockReader.__init__(self, gamestate)

        self.dotastate = self.state['dota'] = {
            'events': [],
            'mode_line': None,
        }

        self.define(0x6B, 'DotaTrigger')

    def handleChatTrigger(self, block, io):
        extract('LL', io)
        message = extractString(io)

        if self.currentPlayer['is_admin'] and\
                self.dotastate['mode_line']==None:
            self.dotastate['mode_line'] = message

    def handleDotaTrigger(self, block, io):
        _ = extractString(io)
        a = extractString(io)
        b = extractString(io)

        if b[0] in ('8', '9'):
            c = extract('4s', io)[0][::-1]
        else:
            c, = extract('L', io)

        self.dotastate['events'].append((
            dotaTime(self.state['gametime']), (a,b,c)))


def get_replay_data(io):
    gamestate = getEmptyGamestate()
    gamestate.update({ 'parsetime': time.asctime(), })
    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    reader.parse(io)
    return gamestate
