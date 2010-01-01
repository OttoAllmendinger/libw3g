from os import mkdir
from os.path import join
from shutil import copy

from libw3g.util import get_replay_id
from libdota.tests.util import get_replay_path

def add(replay_file):
    target_fn = get_replay_path(get_replay_id(replay_file).read())
    copy(replay_file, target_fn)
    print 'added replay %s' % target_fn

if __name__=="__main__":
    import sys
    for f in sys.argv[1:]:
        add(f)
