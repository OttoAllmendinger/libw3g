import codecs, locale, sys
sys.stdout = codecs.getwriter(locale.getdefaultlocale()[1])(sys.stdout, 'replace')

import os
import glob
import json
import traceback

from os.path import join, dirname, exists
from shutil import copy
from pprint import pprint

import libw3g
import libdota

FN_REPLAY = 'replay.w3g'
FN_REPLAYDATA = 'replaydata.json'
FN_METADATA = 'metadata.json'
FN_GAMEDATA = 'gamedata.json'
FN_ERRORS = 'errors.txt'

class DuplicateReplayException(Exception):
    pass

class Replay(object):
    __slots__ = ['replay_id', 'metadata', 'gamedata']
    def __init__(self, replay_id, metadata, gamedata):
        self.replay_id = replay_id
        self.metadata = metadata
        self.gamedata = gamedata

class ReplayDB(object):
    def __init__(self, basedir):
        if not basedir or not exists(basedir):
            raise Exception("basedir does not exists: %s" % basedir)

        self.basedir = basedir
        self.replays = dict((r.replay_id, r) for r in filter(None, (
                self.load_replay(r) for r in self.get_replay_ids())))

    def rp_path(self, replay_id, name):
        return join(self.basedir, replay_id, name)

    def rp_file(self, replay_id, name, mode='r'):
        return file(self.rp_path(replay_id, name), mode)

    def get_replay_ids(self):
        return sorted(os.listdir(self.basedir))

    def load_replay(self, replay_id, cached=True):
        try:
            return Replay(replay_id,
                    self.get_metadata(replay_id),
                    self.get_gamedata(replay_id))
        except:
            return None

    def make_data(self, replay_id, targets=None):
        try:
            targets = targets or ('replaydata', 'gamedata')
            if 'replaydata' in targets:
                self.make_replaydata(replay_id)
            if 'gamedata' in targets:
                self.make_gamedata(replay_id)
        except KeyboardInterrupt:
            raise
        except:
            traceback.print_exc()

    def add_replay(self, data, metadata, force=False):
        replay_id = metadata['replay_id'] = libw3g.get_replay_id(data)
        replay_path = self.rp_path(replay_id, FN_REPLAY)

        if not exists(dirname(replay_path)):
            os.makedirs(dirname(replay_path))
        elif not force:
            raise DuplicateReplayException()

        self.rp_file(replay_id, FN_REPLAY, 'w').write(data)

        try:
            self.set_metadata(replay_id, metadata)
            self.make_replaydata(replay_id)
            self.make_gamedata(replay_id)
            errors = None
        except:
            errors = traceback.format_exc()
        finally:
            self.set_errors(replay_id, errors)


    def set_metadata(self, replay_id, metadata):
        json.dump(metadata, self.rp_file(replay_id, FN_METADATA, 'w'))

    def get_metadata(self, replay_id):
        return json.load(self.rp_file(replay_id, FN_METADATA))


    def make_gamedata(self, replay_id):
        gamedata = libdota.get_gamedata(
                self.get_metadata(replay_id),
                self.get_replaydata(replay_id))
        json.dump(gamedata, self.rp_file(replay_id, FN_GAMEDATA, 'w'))
        return gamedata

    def get_gamedata(self, replay_id):
        return json.load(self.rp_file(replay_id, FN_GAMEDATA))


    def make_replaydata(self, replay_id):
        replaydata = libdota.get_replaydata(
                self.rp_file(replay_id, FN_REPLAY).read())
        json.dump(replaydata, self.rp_file(replay_id, FN_REPLAYDATA, 'w'))

    def get_replaydata(self, replay_id):
        return json.load(self.rp_file(replay_id, FN_REPLAYDATA))


    def get_errors(self, replay_id):
        return self.rp_file(replay_id, FN_ERRORS).read()

    def set_errors(self, replay_id, errors):
        self.rp_file(replay_id, FN_ERRORS, 'w').write(errors or '')



def dump_gamedata(replay, verbose=False):
    print ':: gamedata %s' % replay.replay_id
    print ':: players'
    keys = 'nick', 'team', 'hero'
    print ''.join('%-16s' % k for k in keys)
    print
    for p in replay.gamedata['players'].values():
        print ''.join('%-16s' % p.get(k) for k in keys)

    if verbose:
        pprint(replay.gamedata)


def commandline():
    import optparse
    op = optparse.OptionParser()
    op.add_option('-b', '--basedir')
    op.add_option('-a', '--add-replays', action='store_true')
    op.add_option('-l', '--list', action='store_true')
    op.add_option('-t', '--test', action='store_true')
    op.add_option('-v', '--verbose', action='store_true')

    op.add_option('--dump-gamedata', action='store_true')
    op.add_option('--rebuild', action='store_true')

    options, args = op.parse_args()

    rdb = ReplayDB(options.basedir)

    if options.test:
        test(rdb)

    if options.rebuild:
        replay_ids = rdb.get_replay_ids()
        targets = args
        for n, replay_id in enumerate(replay_ids):
            print 'making data for %s (%d/%d)' % (
                    replay_id, n+1, len(replay_ids))
            rdb.make_data(replay_id, targets)

    if options.add_replays:
        for replay_path in args:
            rp_data = file(replay_path).read()
            replay_id = libw3g.get_replay_id(rp_data)
            print 'adding replay %s...' % replay_id
            try:
                rdb.add_replay(rp_data, {
                    'file_timestamp': libw3g.get_timestamp(replay_path)})
                errors = rdb.get_errors(replay_id)
                if errors:
                    print 'errors: %s' % errors
            except DuplicateReplayException:
                print 'skipped (already exists)'


    if options.list:
        for replay_id in rdb.get_replay_ids():
            print replay_id, ('error' if replay_id not in rdb.replays else '')

    if options.dump_gamedata:
        for replay in rdb.replays.values():
            dump_gamedata(replay, options.verbose)

def purge_metadata():
    rdb = ReplayDB('local/replaydb')
    for replay_id in rdb.get_replay_ids():
        metadata = rdb.get_metadata(replay_id)
        new_metadata = {
                'file_timestamp': metadata.get('file_timestamp'),
                'parse_error': metadata.get('parse_error')
        }
        rdb.set_metadata(replay_id, new_metadata)


if __name__=="__main__":
    commandline()
    #purge_metadata()

