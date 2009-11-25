import os
import os.path as P
import sys
import hashlib
from cStringIO import StringIO
import time
import json
import pprint

from collections import defaultdict

import cherrypy

import parseDota
import DotaUnits


REPLAY_DIR = P.join(P.dirname(__file__), 'replays')
DATA_DIR = P.join(P.dirname(__file__), 'data')

DEBUG_FAKE_UPLOAD_LAG = False

def get_metadata(replay_dir):
    return json.load(file(P.join(REPLAY_DIR, replay_dir, 'fileinfo.json')))

def get_replaydata(replay_dir):
    return json.load(file(P.join(REPLAY_DIR, replay_dir, 'replay.json')))

def get_replay_hashs():
    return os.listdir(P.join(REPLAY_DIR))

def get_replay_dir(replay_file_hash):
    return P.join(REPLAY_DIR, replay_file_hash)

def replay_exists(replay_file_hash):
    return P.exists(get_replay_dir(replay_file_hash))

def get_hero_name(hero_id):
    return DotaUnits.getUnit(unicode(hero_id).encode('utf8')).getName()

def is_valid_replay_hash(replay_hash):
    return all((c in '012345679abcdefg') for c in replay_hash)

class DotaStats:
    def exists(self, replay_file_hash):
        return unicode(replay_exists(replay_file_hash))
    exists.exposed = True

    @cherrypy.expose
    def set_admin(self):
        cherrypy.response.cookie['dotastats-admin'] = 'True'
        return 'cookie data was: %s' % cherrypy.request.cookie

    @cherrypy.expose
    def unset_admin(self):
        cherrypy.response.cookie['dotastats-admin'] = 'False'
        return 'cookie unset'

    def is_admin(self):
        return cherrypy.request.cookie.get('dotastats-admin')=='True'

    @cherrypy.expose
    def dumpjson(self, replay_hash):
        assert is_valid_replay_hash(replay_hash)
        gamedata = get_replaydata(replay_hash)
        return ('<plaintext>'+
                pprint.pformat(gamedata))

    @cherrypy.expose
    def reparse(self, replay_hash):
        assert is_valid_replay_hash(replay_hash)
        fileio = file(P.join(get_replay_dir(replay_hash), 'replay.w3g'), 'r')
        self.parse(fileio, overwrite=True)
        return self.dumpjson(replay_hash)

    @cherrypy.expose
    def index(self):
        buf = [ (
            u'<html><body>'
            u'<ul>') ]

        for replay_hash in get_replay_hashs():
            metadata = get_metadata(replay_hash)
            gamedata = get_replaydata(replay_hash)
            players = [s.get('Name') for s in gamedata['Slots'].values()]
            buf.append(u'<li><a href="/replay/%s">%s (%s)</a>' % (replay_hash,
                time.asctime(time.localtime(metadata['file_timestamp'])),
                u', '.join(players)))
            if self.is_admin() or 1:
                buf.append(' <a href="dumpjson/%s">dump json</a>' % replay_hash)
            buf.append('</li>')

        buf.append('</ul></body></html>')
        return u''.join(buf).encode('utf8')


    @cherrypy.expose
    def replay(self, replay_hash):
        assert is_valid_replay_hash(replay_hash)
        if not replay_exists(replay_hash):
            return 'REPLAY_NOT_FOUND'

        gamedata = get_replaydata(replay_hash)
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
                        slot.get('Name'), get_hero_name(slot.get('Hero')),
                        #stats.get('Kills'), 
                        sum(slot.get('KilledPlayers', {}).values()),
                        slot.get('Deaths'),
                        slot.get('Assists'))) + '</tr>' )
        buf.append('</table>')

        return ''.join(buf).encode('utf8')



    def dump_json(self, replay_hash):
        pass

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
            if DEBUG_FAKE_UPLOAD_LAG:
                time.sleep(0.1)
        yield '-'*8

        replay_file_hash = self.parse(tmpio)
        metadata = {
            'file_timestamp': int(timestamp),
            'upload_timestamp': int(time.time()),
            'uploader_ip': cherrypy.request.remote.ip }
        self.save_metadata(replay_file_hash, metadata)

    def parse(self, replayio, overwrite=False):
        replayio.seek(0)
        state = parseDota.parseDotaReplay(replayio)
        replayio.seek(0)
        replay_file_hash = hashlib.md5(replayio.read()).hexdigest()
        if (not replay_exists(replay_file_hash)) or overwrite:
            replay_dir = get_replay_dir(replay_file_hash)
            if not P.exists(replay_dir):
                os.mkdir(replay_dir)
            uploaded_replay_file = file(P.join(replay_dir, 'replay.w3g'), 'w')
            replayio.seek(0)
            uploaded_replay_file.write(replayio.read())
            replay_state = file(P.join(replay_dir, 'replay.json'), 'w')
            json.dump(state, replay_state)
        return replay_file_hash

    def save_metadata(self, replay_hash, metadata):
        assert is_valid_replay_hash(replay_hash)
        replay_dir = get_replay_dir(replay_hash)
        metadata_file = file(P.join(replay_dir, 'fileinfo.json'), 'w')
        json.dump(metadata, metadata_file)

    @cherrypy.expose
    def highscore(self):
        all_replay_data = [get_replaydata(replay_hash) for replay_hash in get_replay_hashs()]
        kills = defaultdict(int)
        for replay_data in all_replay_data:
            for slot in replay_data['Slots'].values():
                kills[slot['Name']] += sum(
                        slot.get('KilledPlayers', {}).values())
        buf = '<html>'
        buf += '<style type="text/css">'
        buf += '    #highscore { font-size: 200%; font-family: "Georgia" }'
        buf += '    #highscore .name { width: 500px }'
        buf += '</style>'
        buf += '<body><table id="highscore">'
        for player, kills in sorted(kills.items(), key=lambda x: -x[1]):
            buf += '<tr><td class="name">%s</td><td>%s</td></tr>' % (player, kills)
        buf += '</table></body></html>'
        return buf.encode('utf8')


    upload.exposed = True
    upload._cp_config = {'response.stream': True}



app = cherrypy.tree.mount(DotaStats())

if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-p', '--port')
    parser.add_option('--fastcgi', action='store_true')
    options, args = parser.parse_args()
    if options.fastcgi:
        from flup.server.fcgi import WSGIServer
        cherrypy.config.update( {
                    'engine.autoreload_on': False,
                    'tools.sessions.on': True,
                    'log.screen': False,
                    'log.access_file': '/tmp/cherry_access.log',
                    'log.error_file': '/tmp/cherry_error.log'
                })
        WSGIServer(app).run()
    if options.port:
        cherrypy.config.update( {'server.socket_port': int(options.port) } )
    cherrypy.quickstart()

