import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

import logging
import json

from pprint import pprint

from libw3g.Tools import *
from libdota import get_replay_data, get_game_data

def dump_replay_data(replay_data):
    pprint(replay_data)

def dump_state(gamestate):
    pprint(gamestate)

def dump_dota_events(gamestate):
    for ts, event in gamestate['dota']['events']:
        print "%12s | " % formatGametime(ts) + "%-12s, %-12s, %-12s" % event

def dump_metadata(state):
    print 'Header: Version %d.%d - Modeline: %s' % (state['header']['version'],
            state['header']['major_v'], state['dota']['mode_line'])

def dump_results(state):
    print " %9s | %8s | %-12s | %-16s | %-38s | %s/%s/%s" % ("player_id",
            "slot_id", "team", "name", "hero", "kills", "deaths", "assists")
    for s in state['slots'].values():
        kills, deaths, assists = (s.get('kills'), s.get('deaths'),
                s.get('Assists'))
        print ' %9d | %8d | %-12s | %-16s | %-38s | %s/%s/%s' % (
                s.get("player_id"), s.get("slot_id"), s.get("team"), s['name'],
                s['hero'], kills, deaths, assists)

def dump_players(state):
    print '# Name, SlotId, PlayerId, SpawnId, StatId'
    for slot in state['slots'].values():
        print "%-18s : %d %d %d %d" % (slot.get('name'), slot.get('slot_id'),
                slot.get('player_id'), slot.get('spawn_id'),
                slot.get('stat_id'))

def dump_json(state, json_file_name):
    json.dump(state, file(json_file_name, 'w'))

def usage(name):
    print "Usage: %s REPLAY-FILE" % name

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-m', '--metadata', action='store_true')
    parser.add_option('-r', '--replaydata', action='store_true')
    parser.add_option('-g', '--gamedata', action='store_true')
    parser.add_option('-e', '--dota-events', action='store_true')
    #parser.add_option('-s', '--state', action='store_true')
    #parser.add_option('-p', '--players', action='store_true')
    #parser.add_option('-j', '--json')
    options, args = parser.parse_args()

    #meta_data = get_meta_data(args[0])
    replay_data = get_replay_data(file(args[0]))
    game_data = get_game_data(replay_data)

    if options.metadata:
        dump_metadata(meta_data)
    if options.replaydata:
        dump_replay_data(replay_data)
    if options.gamedata:
        dump_state(game_data)
    if options.dota_events:
        dump_dota_events(replay_data)
    #if options.players:
        #dump_players(state)
    #if options.json:
        #dump_json(state, options.json)

