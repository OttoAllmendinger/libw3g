import os
import json
import time
from os.path import join, dirname, exists
from itertools import groupby, chain
import hashlib

import libdota

REPLAY_DIR = join(dirname(__file__), 'replays')

def get_replay_file(replay_hash, mode):
    return file(join(get_replay_dir(replay_hash), 'replay.w3g'), mode)

def get_replay_metadata_file(replay_hash, mode):
    return file(join(get_replay_dir(replay_hash), 'metadata.json'), mode)

def get_replay_dir(replay_hash):
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

def get_replays():
    return map(load_replay_metadata, os.listdir(REPLAY_DIR))

def is_valid_replay(game):
    return (game.get('dota') and game['dota']['game_length']>600)

def get_dota_replays():
    return filter(is_valid_replay, get_replays())

def get_playdays():
    format_ts = lambda fmt, ts: time.strftime(fmt, time.localtime(ts))
    replay_ts = lambda r: r['file_timestamp']
    group_func = lambda r: format_ts('%Y-%m-%d', replay_ts(r))
    mk_play_day = lambda (date, games): dict(
            week_day=format_ts('%A', replay_ts(games[0])),
            date=format_ts('%Y-%m-%d', replay_ts(games[0])), games=games)
    return map(mk_play_day, sorted(((key, list(games))
                for key, games in groupby(sorted(get_dota_replays(),
                    key=replay_ts, reverse=True), group_func)), reverse=True))

def get_players():
    games = get_dota_replays()
    return sorted(
        set(chain(*(g['dota']['players'].keys() for g in games))),
        key=lambda p: (sum(-1 for g in games if p in g['dota']['players']),p))

def get_replay_hash(data):
    return hashlib.md5(data).hexdigest()[:6]

def get_hero_image(hero_id):
    image_file = libdota.DotaUnits.getUnit(
            unicode(hero_id).encode('utf8')).unitData['Art']
    return '/static/' + image_file

def test():
    from betterprint import pprint
    pprint(get_dota_replays())
    #print get_playdays()
    #print get_players()

if __name__=='__main__':
    test()
