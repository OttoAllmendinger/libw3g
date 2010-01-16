import os
import json
import time
from os.path import join, dirname, exists
from itertools import groupby, chain
import hashlib
import logging

import libdota

from libdota.constants import TEAM_1, TEAM_2

def by_name(gamestate, alias_map):
    new_players = {}
    for player_data in add_name(gamestate, alias_map)['players'].values():
        new_players[player_data['name']] = player_data
    gamestate['players'] = new_players
    return gamestate

def add_name(gamestate, alias_map):
    for player in gamestate['players'].values():
        nick = player.get('nick')
        player['name'] = alias_map.get(nick, nick)
    return gamestate

def player_color(player_name):
    return "#%06X" % (hash(player_name) & 0XFFFFFF)

def unalias(gamestate, alias_map):
    #TODO: deprecate
    new_players = {}
    players = dict(gamestate['players'])
    unknown_player = {'nick': 'unknown'}
    nickname = lambda pid: players.get(str(pid), unknown_player)['nick']
    realname = lambda pid: alias_map.get(nickname(pid), nickname(pid))
    logs = 'kill_log', 'death_log'
    for pid, data in players.items():
        new_players[realname(pid)] = players[pid]
        for log in logs:
            data[log] = map(lambda (ts, pid): (ts, realname(pid)), data[log])
            pass
    gamestate['players'] = new_players
    return gamestate

def filter_replays(replays):
    def f(rp):
        return (rp.gamedata['duration']>10*60*1000)
    return sorted(filter(f, replays), key=lambda r: -r.gamedata['start_time'])

def get_player_stats(player_data, gamedata):
    for alias in player_data['aliases']:
        for v in gamedata['players'].values():
            if v['nick']==alias:
                return v

def players_by_team(replay, team):
    return [p for p in replay.gamedata['players'].values() if p['team']==team]

def get_hero_image(hero_id):
    image_file = libdota.DotaUnits.getUnit(
            unicode(hero_id).encode('utf8')).unitData['Image']
    return '/static/images/dota/' + image_file


def get_ministats(replay):
    teamkills = { TEAM_1: 0, TEAM_2: 0 }
    for p in replay.gamedata['players'].values():
        teamkills[p['team']] += len(p['kill_log'])
    return '%d:%d' % (teamkills[TEAM_1], teamkills[TEAM_2])
