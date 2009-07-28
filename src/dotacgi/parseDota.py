#/usr/bin/python
#coding=utf8


# fucking hack
import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

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
from DotaUnits import *


DEBUG = False


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
            self.triggerKeys['8_%d'%i] = ('Inventory', i)

    def handleChatTrigger(self, block, io):
        extract('LL', io)
        message = extractString(io)

        if self.currentPlayer['IsAdmin'] and\
                self.dotastate['ModeLine']==None:
            self.dotastate['ModeLine'] = message

    def handleDotaTrigger(self, block, io):
        drx = extractString(io)
        a = extractString(io)
        b = extractString(io)

        if b[0] in ('8', '9'):
            c = getUnit(extract('4s', io)[0][::-1])
        else:
            c, = extract('L', io)

        if a.isnumeric():
            keyName = self.triggerKeys[b]
            self.dotastate['HeroStats'][int(a)][keyName] = c

        self.dotastate['Events'].append((self.state['gametime'], (a,b,c)))


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
    gamestate = getEmptyGamestate()
    gamestate.update({
            'parsetime': time.asctime(),
    })


    if DEBUG:
        gamestate['debug']['blockdebugger'] = blockDebug

    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    reader.gameBlockReader.actionBlockReader.debug = DEBUG
    reader.parse(io)


    gamestate['DotA']['Hero'] = {}
    for statId, heroStat in gamestate['DotA']['HeroStats'].items():
        heroStat['StatId'] = statId
        slotId = (statId-1) if (statId>6) else statId
        if slotId in gamestate['Slots']:
            gamestate['Slots'][slotId]['Stats'] = heroStat

    return gamestate


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
            state = parseDotaReplay(file(arg))

        dumpState(state)
        dumpSlots(state)

    if len(sys.argv)==1:
        usage(sys.argv[0])

