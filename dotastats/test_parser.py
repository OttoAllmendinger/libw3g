import os.path
import json
import glob
import traceback

import parseDota

def win_msg(string):
    print '\033[32m%s\033[0m' % string

def fail_msg(string):
    print '\033[31m%s\033[0m' % string

def test_replay(replay_file_name):
    replay_file = file(replay_file_name)
    state = parseDota.parseDotaReplay(replay_file)
    reference_file = ('test-data/' +
            os.path.splitext(os.path.basename(replay_file_name))[0] + '.json')
    reference_data = json.load(file(reference_file))

    for player in state['Slots'].values():
        name = player['Name']
        team = player['Team']
        line= '%16s %16s %16s' % (name, team, reference_data[name]['team'])
        if team==reference_data[name]['team']:
            win_msg(line)
        else:
            fail_msg(line)


def test():
    replays = sorted(glob.glob("replay/*w3g"))
    for rp in replays:
        try:
            test_replay(rp)
            print '%s: WIN' % rp
        except Exception, init:
            print '%s: FAIL' % rp
            traceback.print_exc()
        print '\n\n'

if __name__=="__main__":
    test()
