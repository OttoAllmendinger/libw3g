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
                'events': [],
                'mode_line': None,
                'hero_stats': dict((n,{}) for n in range(1, 13)),
        }

        self.state['dota'] = self.dotastate

        self.define(0x6B, 'DotaTrigger')


        self.triggerKeys = {
            '1' : 'kills',
            '2' : 'Deaths',
            '3' : 'creep_kills',
            '4' : 'creep_denies',
            '5' : 'assists',
            '6' : 'end_gold',
            '7' : 'neutrals',
            '9' : 'hero',
            'id': 'spawn_id',
        }

        for i in range(6):
            self.triggerKeys['8_%d'%i] = 'inventory_%d' % i

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

        if a=='Data' and b.startswith('Hero'):
            killedHeroStatId = int(b[-1])
            killerHeroStatId = int(c)
            if killerHeroStatId in self.dotastate['hero_stats']:
                killerStats = self.dotastate['hero_stats'][killerHeroStatId]
            else:
                killerStats = {} # FIXME: dummy dict
            if not 'killed_players' in killerStats:
                killerStats['killed_players'] = {}
            if not killedHeroStatId in killerStats['killed_players']:
                killerStats['killed_players'][killedHeroStatId] = 0
            killerStats['killed_players'][killedHeroStatId] += 1
        elif a.isnumeric():
            keyName = self.triggerKeys[b]
            self.dotastate['hero_stats'][int(a)][keyName] = c

        self.dotastate['events'].append((
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


    gamestate['dota']['hero'] = {}
    for statId, heroStat in gamestate['dota']['hero_stats'].items():
        heroStat['stat_id'] = statId
        slotId = (statId-1) if (statId>6) else statId
        if slotId in gamestate['slots']:
            gamestate['slots'][slotId].update(heroStat)
            if 'spawn_id' in heroStat:
                gamestate['slots'][slotId]['team'] = (
                    'The Sentinel' if heroStat['spawn_id']<6 else 'The Scourge')

    return gamestate


def getDotaStats(io):
    gamestate = getDotaReplay(io)


def get_gamestate(io):
    return parseDotaReplay(io)
