#/usr/bin/python
#coding=utf8

try:
    import psyco
    #psyco.full()
except ImportError:
    print 'install psyco for speedup'

import time
import json
import re

from cStringIO import StringIO
from pprint import pprint
from datetime import timedelta
from logging import basicConfig

from libw3g.ReplayReader import ReplayReader
from libw3g.ActionBlockReader import ActionBlockReader

from libw3g.Tools import *
from DotaUnits import *

from collections import defaultdict

VALID_VERSIONS = ('v6.64')

TEAM_1 = 'The Sentinel'
TEAM_2 = 'The Scourge'

OPPONENT = { TEAM_1: TEAM_2, TEAM_2: TEAM_1 }

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


def parseDotaReplay(io):
    gamestate = getEmptyGamestate()
    gamestate.update({ 'parsetime': time.asctime(), })
    reader = ReplayReader(gamestate)
    reader.gameBlockReader.actionBlockReader = DotaActionBlockReader(gamestate)
    reader.parse(io)
    return gamestate


def get_winner_by_kill_difference(gamestate, min_diff=5):
    team_kills = defaultdict(int)
    for p in gamestate['slots'].values():
        team_kills[p['team']] += p['kills']

    if team_kills[TEAM_1]>(team_kills[TEAM_2]+min_diff):
        return TEAM_1
    elif team_kills[TEAM_2]>(team_kills[TEAM_1]+min_diff):
        return TEAM_2

def get_winner_by_first_leave(gamestate):
    _, player_id, _, _ = gamestate['leaves'][0]
    leaving_player = next(iter(filter(lambda p: p['player_id']==player_id,
        gamestate['players'].values())))
    loser_team = leaving_player['team']
    return OPPONENT[leaving_player['team']]

def get_winner_team(gamestate):
    algorithms = (
            get_winner_by_kill_difference,
            get_winner_by_first_leave)
    for a in algorithms:
        winner_team = a(gamestate)
        if winner_team:
            return winner_team


def get_gameinfo(io):
    dota_version = "Unknown"
    try:
        io.seek(0)
        gamestate = parseDotaReplay(io)
        rx_dota_version = re.search(
                'DotA Allstars (.*?)\.w3x', gamestate['info']['map_name'])

        if rx_dota_version:
            dota_version = rx_dota_version.group(1)
            gamestate['dota']['version'] = dota_version
            assert dota_version in VALID_VERSIONS

        for stat_id, hero_stat in gamestate['dota']['hero_stats'].items():
            hero_stat['stat_id'] = stat_id
            slot_id = (stat_id-1) if (stat_id>6) else stat_id
            if slot_id in gamestate['slots']:
                gamestate['slots'][slot_id].update(hero_stat)
                if 'spawn_id' in hero_stat:
                    gamestate['slots'][slot_id]['team'] = (
                        TEAM_1 if hero_stat['spawn_id']<6 else TEAM_2)

        players = gamestate['players'].values()

        for p in players:
            p['kills'] = sum(p.get('killed_players', {}).values())

        winner_team = get_winner_team(gamestate)

        for p in players:
            p['is_winner'] = p['team']==winner_team

        gamestate.update({
            'players':
                dict((p['name'], p) for p in gamestate['slots'].values()),
            'game_length': gamestate['gametime'] / 1000,
        })

        return gamestate
    except AssertionError:
        raise Exception("Unsupported DotA Version (%s)" % dota_version)
    except:
        raise
