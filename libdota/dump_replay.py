import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

import traceback
import logging
import json

from pprint import pprint

from libw3g.Tools import *
from libw3g import get_timestamp
from libdota import get_replaydata, get_gamedata

def dump_replay_data(replay_data):
    pprint(replay_data)

def dump_state(gamestate):
    pprint(gamestate)

def dump_dota_events(gamestate):
    for ts, event in gamestate['dota_events']:
        print "%12s | " % formatGametime(ts) + "%-12s, %-12s, %-12s" % event

def dump_metadata(replay_data, game_data):
    print 'Header: Version %d.%d' % (replay_data['header']['version'],
            replay_data['header']['major_v'])
    print 'Modes: %s' % (game_data['modes'])

def dump_player_stats(game_data):
    print " %-12s | %-16s | %-8s | %4s/%4s/%4s" % ("team", "nick",
            "hero", "k", "d", "a")
    for p in game_data['players'].values():
        print ' %-12s | %-16s | %-8s | %4s/%4s/%4s' % (
                p["team"], p['nick'], p['hero'],
                len(p['kill_log']), len(p['death_log']), p.get("assists"))

def dump_players(state):
    print '# Name, SlotId, PlayerId, SpawnId, StatId'
    for slot in state['slots'].values():
        print "%-18s : %d %d %d %d" % (slot.get('name'), slot.get('slot_id'),
                slot.get('player_id'), slot.get('spawn_id'),
                slot.get('stat_id'))

def dump_json(state, json_file_name):
    json.dump(state, file(json_file_name, 'w'))

def dump_rdnode(replay_data, rdv):
    nodepath = rdv.split('.')
    node = replay_data
    for name in nodepath:
        node = node[name]
    print '%s=%s' % (rdv, node)

def get_metadata(filename):
    pass

def usage(name):
    print "Usage: %s REPLAY-FILE" % name

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-m', '--meta-data', action='store_true')
    parser.add_option('-r', '--replay-data', action='store_true')
    parser.add_option('-g', '--game-data', action='store_true')
    parser.add_option('-e', '--dota-events', action='store_true')
    parser.add_option('--player-stats', action='store_true')
    parser.add_option('--rd-node')
    #parser.add_option('-s', '--state', action='store_true')
    #parser.add_option('-p', '--players', action='store_true')
    #parser.add_option('-j', '--json')
    options, args = parser.parse_args()

    for arg in args:
        try:
            replay_data = get_replaydata(file(arg).read())
            game_data = get_gamedata(replay_data, get_timestamp(arg))

            if options.meta_data:
                dump_metadata(replay_data, game_data)
            if options.replay_data:
                dump_replay_data(replay_data)
            if options.game_data:
                dump_state(game_data)
            if options.dota_events:
                dump_dota_events(replay_data)
            if options.player_stats:
                dump_player_stats(game_data)
            if options.rd_node:
                dump_rdnode(replay_data, options.rd_node)
            #if options.json:
                #dump_json(state, options.json)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

