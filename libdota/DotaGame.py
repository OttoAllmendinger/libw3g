import re
from libdota import DotaParser
from collections import defaultdict

from libdota.constants import TEAM_1, TEAM_2

VALID_VERSIONS = ('v6.64', )

OPPONENT = { TEAM_1: TEAM_2, TEAM_2: TEAM_1 }

def get_slot_id(stat_id):
    return (stat_id-1) if (stat_id>6) else stat_id

def get_stat_id(slot_id):
    return (slot_id+1) if (slot_id>5) else slot_id

def get_dota_version(replay_data):
    try:
        return re.search('DotA Allstars (.*?)\.w3x',
                replay_data['info']['map_name']).group(1)
    except:
        raise Exception("Couldn't determine DotA version")

def get_modes(event_data):
    modeline = event_data['global_data'].get('modeline', '')
    modes = []
    mode_map = {
        'mm': 'mirror_match',
        'em': 'easy_mode',
        'ar': 'all_random',
        'sp': 'shuffle_players',
        'nb': 'no_bottom',
        'nt': 'no_top',
        'ap': 'all_pick',
    }
    while modeline:
        m, modeline = modeline[:2], modeline[2:]
        if m in mode_map:
            modes.append(mode_map[m])
    return modes

def get_winner_by_dota_event(replay_data, event_data, player_info):
    winner_id = event_data['global_data'].get('Winner')
    return (TEAM_1 if winner_id==1 else TEAM_2)

def get_winner_by_kill_difference(
        replay_data, event_data, player_info, min_diff=5):
    team_kills = defaultdict(int)
    for p in player_info.values():
        if 'team' in p.keys():
            team_kills[p['team']] += len(p['kill_log'])

    if team_kills[TEAM_1]>(team_kills[TEAM_2]+min_diff):
        return TEAM_1
    elif team_kills[TEAM_2]>(team_kills[TEAM_1]+min_diff):
        return TEAM_2

def get_winner_by_first_leave(replay_data, event_data, player_info):
    _, player_id, _, _ = replay_data['leaves'][0]
    leaving_players = filter(lambda p: p['player_id']==player_id,
            player_info.values())
    try:
        leaving_player = next(iter(leaving_players))
        loser_team = leaving_player['team']
        return OPPONENT[loser_team]
    except StopIteration:
        leaving_player = None

def get_winner_team(replay_data, event_data, player_info):
    algorithms = (
            get_winner_by_dota_event,
            get_winner_by_kill_difference,
            get_winner_by_first_leave)
    for alg in algorithms:
        winner_team = alg(replay_data, event_data, player_info)
        if winner_team:
            return winner_team

def get_event_data(replay_data):
    key_names = {
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

    key_names.update(('8_%d' % i, 'inventory_%d' % i) for i in range(6))

    global_data = {}
    hero_data = defaultdict(lambda: defaultdict(list))

    for ts, (a, b, c) in replay_data['dota_events']:
        if a=='Data' and b.startswith('Mode'):
            global_data['modeline'] = b[4:]
        if a=='Data' and b.startswith('Hero'):
            victim_id = int(b.replace('Hero',''))
            killer_id = int(c)
            hero_data[killer_id]['kill_log'].append((ts, victim_id))
            hero_data[victim_id]['death_log'].append((ts, killer_id))
        elif a=='Data' and b.startswith('Level'):
            hero_level = int(b.replace('Level', ''))
            hero_data[int(c)]['level_log'].append((ts, hero_level))
        elif a=='Data' and b.startswith('PUI_'):
            hero_id = int(b.replace('PUI_', ''))
            hero_data[hero_id]['item_log'].append((ts, 'PUI', c))
        elif a=='Data' and b.startswith('DRI_'):
            hero_id = int(b.replace('DRI_', ''))
            hero_data[hero_id]['item_log'].append((ts, 'DRI', c))
        elif a.isnumeric():
            hero_data[int(a)][key_names[str(b)]] = c
        elif a=='Global': # very rare
            global_data[b] = c

    return {
        'hero_data': hero_data,
        'global_data': global_data }

def get_players_info(replay_data, event_data):
    player_info = {}

    slots = dict((p['slot_id'], p) for p in replay_data['players'].values())

    player_data = ((hero_id, slots.get(get_slot_id(hero_id)), hero_data)
            for hero_id, hero_data in event_data['hero_data'].items()
                    if (hero_data.get('hero')))

    for hero_id, slot_data, hero_data in player_data:
        player_info[hero_id] = {
            'nick': slot_data['name'],
            'player_id': slot_data['player_id'],
            'hero': hero_data['hero'],
            'item_log': hero_data['item_log'],
            'kill_log': hero_data['kill_log'],
            'death_log': hero_data['death_log'],
            'level_log': hero_data['level_log'],
            'team': (TEAM_1 if hero_data['spawn_id']<6 else TEAM_2),
            'inventory': [hero_data.get('inventory_%d'%i) for i in range(6)],
        }

    winner_team = get_winner_team(replay_data, event_data, player_info)

    for player_data in player_info.values():
        player_data['is_winner'] = (player_data['team']==winner_team)

    return player_info

def get_gamedata(meta_data, replay_data):
    if 'dota_events' not in replay_data:
        raise Exception("no dota events found")
    elif not get_dota_version(replay_data) in VALID_VERSIONS:
        raise Exception("unsupported DotA Version" %
                get_dota_version(replay_data))

    event_data = get_event_data(replay_data)

    return {
        'start_time':
            meta_data['file_timestamp']-replay_data['gametime']/1000,
        'replay_id': replay_data['replay_id'],
        'duration': replay_data['gametime'],
        'players': get_players_info(replay_data, event_data),
        'global': event_data['global_data'],
        'modes': get_modes(event_data)
    }
