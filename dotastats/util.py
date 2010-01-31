import os
import json
import time
from os.path import join, dirname, exists
from itertools import groupby, chain
import hashlib
import logging

from collections import defaultdict

import libdota

from libdota.constants import TEAM_1, TEAM_2

from ReplayDB import ReplayDB
from PlayerDB import PlayerDB

_replaydb = ReplayDB(join(dirname(__file__), 'data', 'replaydb'))
_playerdb = PlayerDB(join(dirname(__file__), 'data', 'playerdb'))

def get_replays():
    return filter_replays(get_all_replays())

def get_all_replays():
    return map(by_name, _replaydb.replays.values())

def get_players():
    return _playerdb.players

def by_name(replay):
    new_players = {}
    for player_data in add_name(replay.gamedata)['players'].values():
        new_players[player_data['name']] = player_data
    replay.gamedata['players'] = new_players
    return replay

def add_name(gamestate):
    for player in gamestate['players'].values():
        nick = player.get('nick')
        player['name'] = _playerdb.alias_map.get(nick, nick)
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

def players_by_team(replay, team):
    return [p for p in replay.gamedata['players'].values() if p['team']==team]

def get_hero_image(hero_id):
    return get_unit_image(hero_id)

def get_unit_image(unit_id):
    image_file = libdota.DotaUnits.getUnit(
            unicode(unit_id).encode('utf8')).unitData['Image']
    return '/static/images/dota/' + image_file


def get_ministats(replay):
    teamkills = { TEAM_1: 0, TEAM_2: 0 }
    for p in replay.gamedata['players'].values():
        teamkills[p['team']] += len(p['kill_log'])
    return '%d:%d' % (teamkills[TEAM_1], teamkills[TEAM_2])


def wintag(player):
    return 'win' if player['is_winner'] else 'fail'



def players_by_name(players):
    return dict((p['name'], p) for p in players.values())

def get_player_score(player_stat):
    return (player_stat['kills'] * 100 -
            player_stat['deaths'] * 100 +
            player_stat['assists'] * 20)

def get_player_stats(players, replays):
    player_stats = dict(
            (p, defaultdict(int)) for p in players)

    for replay in replays:
        players = players_by_name(replay.gamedata['players'])
        for name in players:
            player = players.get(name)
            if player:
                player_stats[name]['kills'] += len(player['kill_log'])
                player_stats[name]['deaths'] += len(player['death_log'])
                player_stats[name]['assists'] += len(player['assist_log'])

    for player_stat in player_stats.values():
        player_stat['score'] = get_player_score(player_stat)

    return player_stats

