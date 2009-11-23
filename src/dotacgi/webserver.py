import os
import os.path as P
import hashlib
from cStringIO import StringIO
import time
import json

import cherrypy


import parseDota
import DotaUnits

REPLAY_DIR = P.join(P.dirname(__file__), 'replays')

def get_metadata(replay_dir):
    return json.load(file(P.join(REPLAY_DIR, replay_dir, 'fileinfo.json')))

def get_replaydata(replay_dir):
    return json.load(file(P.join(REPLAY_DIR, replay_dir, 'replay.json')))

def get_replay_dirs():
    return os.listdir(P.join(REPLAY_DIR))

def replay_exists(replay_file_hash):
    return P.exists(P.join(REPLAY_DIR, replay_file_hash))

def get_hero_name(hero_id):
    return DotaUnits.getUnit(unicode(hero_id).encode('utf8')).getName()


class DotaStats:
    def exists(self, replay_file_hash):
        return unicode(replay_exists(replay_file_hash))
    exists.exposed = True

    def index(self):
        buf = [ (
            u'<html><body>'
            u'<ul>') ]

        for replay_dir in get_replay_dirs():
            metadata = get_metadata(replay_dir)
            gamedata = get_replaydata(replay_dir)
            players = [s.get('Name') for s in gamedata['Slots'].values()]
            buf.append(u'<li><a href="/replay/%s">%s (%s)</li>' % (replay_dir,
                time.asctime(time.localtime(metadata['file_timestamp'])),
                u', '.join(players)))

        buf.append('</ul></body></html>')
        return u''.join(buf).encode('utf8')
    index.exposed = True


    def replay(self, replay_dir):
        gamedata = get_replaydata(replay_dir)
        buf = [('<html><body><table>'
                '<tr>'
                '<th>Name</th>'
                '<th>Hero</th>'
                '<th>Kills</th>'
                '<th>Deaths</th>'
                '<th>Assists</th>'
                '</tr>')]
        for slot in gamedata['Slots'].values():
            stats = slot.get('Stats', {})
            buf.append(
                    '<tr>' +
                    ''.join('<td>%s</td>' % v for v in (
                        slot.get('Name'), get_hero_name(stats.get('Hero')),
                        stats.get('Kills'), stats.get('Deaths'),
                        stats.get('Assists'))) + '</tr>' )
        buf.append('</table>')

        return ''.join(buf).encode('utf8')

    replay.exposed = True

    def upload(self, replay_file=None, timestamp=None):
        timestamp = int(timestamp)

        size = 0
        tmpio = StringIO()
        while True:
            data = replay_file.file.read(8192)
            size += len(data)
            if not data:
                break
            else:
                tmpio.write(data)
                yield "%8d" % size
        yield '-'*8

        tmpio.seek(0)
        state = parseDota.parseDotaReplay(tmpio)
        tmpio.seek(0)
        replay_file_hash = hashlib.md5(tmpio.read()).hexdigest()
        if not replay_exists(replay_file_hash):
            replay_dir = P.join(REPLAY_DIR, replay_file_hash)
            os.mkdir(replay_dir)
            uploaded_replay_file = file(P.join(replay_dir, 'replay.w3g'), 'w')
            tmpio.seek(0)
            uploaded_replay_file.write(tmpio.read())
            replay_state = file(P.join(replay_dir, 'replay.json'), 'w')
            json.dump(state, replay_state)
            metadata_file = file(P.join(replay_dir, 'fileinfo.json'), 'w')
            json.dump({
                'file_timestamp': int(timestamp),
                'upload_timestamp': int(time.time()),
                'uploader_ip': cherrypy.request.remote.ip }, metadata_file)



    upload.exposed = True
    upload._cp_config = {'response.stream': True}



cherrypy.tree.mount(DotaStats())

if __name__=='__main__':
    cherrypy.quickstart()

