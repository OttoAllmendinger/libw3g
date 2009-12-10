import os
import json
import time
from os.path import join, dirname, exists
from itertools import groupby, chain
import hashlib
import logging

import libdota

REPLAY_DIR = join(dirname(__file__), 'replays')

def get_replay_file(replay_hash, mode):
    return file(join(get_replay_dir(replay_hash), 'replay.w3g'), mode)

def get_replay_metadata_file(replay_hash, mode):
    return file(join(get_replay_dir(replay_hash), 'metadata.json'), mode)

def get_replay_dir(replay_hash):
    assert all((c in '0123456789abcdef') for c in replay_hash)
    return join(REPLAY_DIR, replay_hash)

def replay_exists(replay_hash):
    return exists(get_replay_dir(replay_hash))

def save_replay(replay_hash, data):
    if replay_exists(replay_hash):
        raise Exception('replay already exists')
    else:
        replay_dir = get_replay_dir(replay_hash)
        os.mkdir(replay_dir)
        get_replay_file(replay_hash, 'w').write(data)

def save_replay_metadata(replay_hash, metadata):
    json.dump(metadata, get_replay_metadata_file(replay_hash, 'w'))

def load_replay_metadata(replay_hash):
    try:
        return json.load(get_replay_metadata_file(replay_hash, 'r'))
    except:
        return {}

def get_game_data(metadata):
    game = {'players':{}}
    players = metadata['dota']['info']['players']
    game['replayHash'] = metadata['replay_hash']
    players_kid = dict((p['stat_id'], p) for p in players.values())
    for player in players.values():
        game['players'][player['name']] = {
                'heroId': player['hero'],
                'isWinner': player['is_winner'],
                'kills': player['kills'],
                'killedPlayers': dict(
                    (players_kid.get(int(k), {}).get('name'), v) for k,v in
                    player.get('killed_players', {}).items()),
                'team': player.get('team'),
                'levelLog': player.get('level_log', []),
                'killLog': player.get('kill_log', []),
                'deathLog': player.get('death_log', []),
        }
    game['duration'] = metadata['dota']['game_length']
    game['endTime'] = metadata['file_timestamp']
    game['startTime'] = game['endTime'] - game['duration']
    return game

def get_replays():
    return map(load_replay_metadata, os.listdir(REPLAY_DIR))

def is_valid_replay(game):
    return (game.get('dota') and game['dota']['game_length']>600)

def get_dota_replays():
    replays = {}
    for metadata in filter(is_valid_replay, get_replays()):
        try:
            game = get_game_data(metadata)
            replays[game['replayHash']] = game
        except:
            logging.exception('invalid replay')
    return replays

def get_playdays():
    format_ts = lambda fmt, ts: time.strftime(fmt, time.gmtime(ts))
    replay_ts = lambda r: r['startTime']
    group_func = lambda r: format_ts('%Y-%m-%d', replay_ts(r))
    mk_play_day = lambda (date, games): dict(
            week_day=format_ts('%A', replay_ts(games[0])),
            date=format_ts('%Y-%m-%d', replay_ts(games[0])), games=games)
    return map(mk_play_day, sorted(((key, list(games))
                for key, games in groupby(sorted(get_dota_replays().values(),
                    key=replay_ts, reverse=True), group_func)), reverse=True))

def get_players():
    games = get_dota_replays().values()
    return sorted(
        set(chain(*(g['players'].keys() for g in games))),
        key=lambda p: (sum(-1 for g in games if p in g['players']), p))

def get_replay_hash(data):
    return hashlib.md5(data).hexdigest()[:6]

def get_hero_image(hero_id):
    image_file = libdota.DotaUnits.getUnit(
            unicode(hero_id).encode('utf8')).unitData['Image']
    return '/static/images/' + image_file

def test():
    from betterprint import pprint
    pprint(get_dota_replays())
    pprint(get_playdays())
    #print get_players()

if __name__=='__main__':
    test()
