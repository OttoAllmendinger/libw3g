import json
import traceback
from pprint import pprint

from libdota import get_replay_data, get_game_data
from libdota.tests.util import get_replay_ids, get_replay_path, get_test_data


TEAM_1 = u'The Sentinel'
TEAM_2 = u'The Scourge'

def test_teams():
    test_data = get_test_data('test_teams')
    for replay_id, ref_teams in test_data.items():
        replay_data = get_replay_data(file(get_replay_path(replay_id)))
        game_data = get_game_data(replay_data)
        teams = get_teams(game_data)
        print teams
        print ref_teams
        print (sorted(teams[TEAM_1])==sorted(ref_teams[TEAM_1]) and
                sorted(teams[TEAM_2])==sorted(ref_teams[TEAM_2]))

def get_teams(game_data):
    teams = {TEAM_1: [], TEAM_2: []}
    for player in game_data['players'].values():
        teams[player['team']].append(player['nick'])
    return teams


def dump_teams():
    replay_teams = {}
    for replay_id in get_replay_ids():
        try:
            replay_data = get_replay_data(file(get_replay_path(replay_id)))
            game_data = get_game_data(replay_data)
            if 'shuffle_players' in game_data['modes']:
                replay_teams[replay_id] = get_teams(game_data)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()
            pass
    pprint(replay_teams)

if __name__=="__main__":
    test_teams()
