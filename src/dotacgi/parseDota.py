#/usr/bin/python
#coding=utf8

try:
    import psyco
    psyco.full()
except ImportError:
    print 'install psyco for speedup'

import time
import json

from pprint import pprint
from datetime import timedelta
from logging import basicConfig

from libw3g.ReplayReader import ReplayReader
from libw3g.ActionBlockReader import ActionBlockReader

from libw3g.Tools import *


from DotaUnits import *


DEBUG = True

def dotaTime(t):
    return t # TODO: fix timing issues?

class DotaActionBlockReader(ActionBlockReader):
    def __init__(self, gamestate):
        ActionBlockReader.__init__(self, gamestate)

        self.dotastate = {
                'Events': [],
                'ModeLine': None,
                'HeroStats': dict((n,{}) for n in range(1, 13)),
                'MapPlayerHero': {},
                'MapHeroPlayer': {}
        }

        self.state['DotA'] = self.dotastate

        self.define(0x6B, 'DotaTrigger')


        self.triggerKeys = {
            '1' : 'Kills',
            '2' : 'Deaths',
            '3' : 'Creep Kills',
            '4' : 'Creep Denies',
            '5' : 'Assists',
            '6' : 'End Gold',
            '7' : 'Neutrals',
            '9' : 'Hero',
            'id': 'SpawnId',
        }

        for i in range(6):
            self.triggerKeys['8_%d'%i] = 'Inventory%d' % i

    def handleChatTrigger(self, block, io):
        extract('LL', io)
        message = extractString(io)

        if self.currentPlayer['IsAdmin'] and\
                self.dotastate['ModeLine']==None:
            self.dotastate['ModeLine'] = message

    def handleDotaTrigger(self, block, io):
        _ = extractString(io)
        a = extractString(io)
        b = extractString(io)

        if b[0] in ('8', '9'):
            c = extract('4s', io)[0][::-1]
        else:
            c, = extract('L', io)

        if a=='Data' and b.startswith('Hero'):
            killedHeroStatId = int(b[-1])
            killerHeroStatId = int(c)
            '''
            print '%s: %s kills %s' % (formatGametime(
                    dotaTime(self.state['gametime'])),
                    killerHeroStatId, killedHeroStatId)
            '''
            if killerHeroStatId in self.dotastate['HeroStats']:
                killerStats = self.dotastate['HeroStats'][killerHeroStatId]
            else:
                killerStats = {} # FIXME: dummy dict
            if not 'KilledPlayers' in killerStats:
                killerStats['KilledPlayers'] = {}
            if not killedHeroStatId in killerStats['KilledPlayers']:
                killerStats['KilledPlayers'][killedHeroStatId] = 0
            killerStats['KilledPlayers'][killedHeroStatId] += 1
        elif a.isnumeric():
            keyName = self.triggerKeys[b]
            self.dotastate['HeroStats'][int(a)][keyName] = c

        self.dotastate['Events'].append((
            dotaTime(self.state['gametime']), (a,b,c)))



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

def dumpBlock(reader, block, io):
    return
    print "%s : block %s" % (formatGametime(reader.state['gametime']), block)


def parseDotaReplay(io):
    gamestate = getEmptyGamestate()
    gamestate.update({
            'parsetime': time.asctime(),
    })


    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    reader.gameBlockReader.debug = DEBUG
    reader.gameBlockReader.actionBlockReader.debug = DEBUG
    reader.parse(io)


    gamestate['DotA']['Hero'] = {}
    for statId, heroStat in gamestate['DotA']['HeroStats'].items():
        heroStat['StatId'] = statId
        slotId = (statId-1) if (statId>6) else statId
        if slotId in gamestate['Slots']:
            gamestate['Slots'][slotId].update(heroStat)
            if 'SpawnId' in heroStat:
                gamestate['Slots'][slotId]['Team'] = (
                    'The Sentinel' if heroStat['SpawnId']<6 else 'The Scourge')

    return gamestate


def getDotaStats(io):
    gamestate = getDotaReplay(io)

