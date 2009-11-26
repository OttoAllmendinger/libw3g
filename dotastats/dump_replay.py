import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

import logging
import json

try:
    from betterprint import pprint
except ImportError:
    from pprint import pprint

from libw3g.Tools import *

import parseDota


def dump_state(gamestate):
    pprint(gamestate)

def dump_events(gamestate):
    print '---- events ----'
    for ts, event in gamestate['DotA']['Events']:
        print "%12s | " % formatGametime(ts) + "%-12s, %-12s, %-12s" % event

def dump_metadata(state):
    print 'Header: Version %d.%d - Modeline: %s' % (state['header']['version'],
            state['header']['major_v'], state['DotA']['ModeLine'])

def dump_results(state):
    print " %8s | %8s | %-12s | %-16s | %-38s | %s/%s/%s" % ("PlayerId",
            "SlotId", "Team", "Name", "Hero", "Kills", "Deaths", "Assists")
    for s in state['Slots'].values():
        stats = s['Stats']
        kills, deaths, assists = (stats.get('Kills'), stats.get('Deaths'),
                stats.get('Assists'))
        print ' %8d | %8d | %-12s | %-16s | %-38s | %s/%s/%s' % (
                s.get("PlayerId"), s.get("SlotId"), s.get("Team"), s['Name'],
                stats['Hero'], kills, deaths, assists)

def dump_players(state):
    print '# Name, SlotId, PlayerId, SpawnId, StatId'
    for slot in state['Slots'].values():
        stats = slot.get('Stats', {})
        print "%-18s : %d %d %d %d" % (slot.get('Name'), slot.get('SlotId'),
                slot.get('PlayerId'), stats.get('SpawnId'), stats.get('StatId'))

def dump_json(state, json_file_name):
    json.dump(state, file(json_file_name, 'w'))


def usage(name):
    print "Usage: %s REPLAY-FILE" % name


if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-r', '--results', action='store_true')
    parser.add_option('-e', '--events', action='store_true')
    parser.add_option('-s', '--state', action='store_true')
    parser.add_option('-m', '--metadata', action='store_true')
    parser.add_option('-p', '--players', action='store_true')
    parser.add_option('-j', '--json')
    options, args = parser.parse_args()

    state = parseDota.parseDotaReplay(file(args[0]))

    if options.metadata:
        dump_metadata(state)
    if options.results:
        dump_results(state)
    if options.state:
        dump_state(state)
    if options.events:
        dump_events(state)
    if options.players:
        dump_players(state)
    if options.json:
        dump_json(state, options.json)

