import json
from os.path import dirname, join, exists
from os import listdir

_replay_dir = join(dirname(__file__), 'replays')

_test_data_dir = join(dirname(__file__), 'test-data')

if not exists(_replay_dir):
    mkdir(_replay_dir)

def get_replay_dir():
    return _replay_dir

def get_replay_path(replay_id):
    return join(_replay_dir, 'rp_%s.w3g' % replay_id)

def get_replay_ids():
    return (r.replace('rp_', '').replace('.w3g', '')
                for r in listdir(_replay_dir))

def get_test_data(test_data_name):
    return json.load(file(join(_test_data_dir, '%s.json' % test_data_name)))
