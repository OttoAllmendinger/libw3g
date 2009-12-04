import os
import sys
import time
import logging
from os.path import abspath, dirname, exists, join
from cStringIO import StringIO

import cherrypy
from genshi.template import TemplateLoader

import libw3g
import libw3g.Tools
import libdota.DotaParser
import libdota.DotaUnits
from dotastats.util import *



# TODO: maybe add http://www.thomasfrank.se/json_editor.html

loader = TemplateLoader(join(dirname(__file__), 'html'), auto_reload=True)

class DotaStats:
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
    def exists(self, file_hash):
        return unicode(replay_exists(file_hash))

    @cherrypy.expose
    def upload(self, replay_file=None, timestamp=None):
        timestamp, size, tmp_io = int(timestamp), 0, StringIO()

        while True:
            chunk = replay_file.file.read(8192)
            size += len(chunk)
            if not chunk:
                break
            else:
                tmp_io.write(chunk)
                yield "%8d" % size
        yield '-'*8

        tmp_io.seek(0)
        data = tmp_io.read()
        replay_hash = get_replay_hash(data)

        save_replay(replay_hash, data)
        save_replay_metadata(replay_hash, {
            'replay_hash': replay_hash,
            'file_timestamp': int(timestamp),
            'upload_timestamp': int(time.time()),
            'uploader_ip': cherrypy.request.remote.ip,
            'dota': libdota.get_gameinfo(tmp_io) })

    upload._cp_config = {'response.stream': True}

    @cherrypy.expose
    def game_data(self, **k):
        games = {}
        for full_info in get_dota_replays():
            games[full_info['replay_hash']] = game = {}
            for player in full_info['dota']['info']['players'].values():
                game[player['name']] = {'heroId': player['hero']}
        return json.dumps(games)

    @cherrypy.expose
    def reparse_all(self):
        for replay_hash in os.listdir(REPLAY_DIR):
            replay_file = get_replay_file(replay_hash, 'r')
            replay_metadata = load_replay_metadata(replay_hash)
            replay_metadata['dota'] = None
            try:
                replay_metadata['dota'] = libdota.get_gameinfo(replay_file)
            except:
                logging.exception('failed to parse replay')
            finally:
                save_replay_metadata(replay_hash, replay_metadata)
                yield '%s %s<br>' % (replay_hash, bool(replay_metadata['dota']))

    @cherrypy.expose
    def index(self):
        return loader.load('overview.tpl.html').generate(
                playdays=get_playdays(), players=get_players(),
                get_hero_image=get_hero_image,
                libw3g_version=libw3g.version).render('html')

    @cherrypy.expose
    def static(self):
        return "you shouldn't see this"



if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-p', '--port')
    parser.add_option('--fastcgi', action='store_true')
    options, args = parser.parse_args()

    config = {
        '/': {
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf8',
            'tools.encode.add_charset': True,
            'tools.staticdir.root': join(dirname(abspath(__file__)))},
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static' }}

    if options.fastcgi:
        from flup.server.fcgi import WSGIServer
        cherrypy.config.update( {
                    'engine.autoreload_on': False,
                    'tools.sessions.on': True,
                    'log.screen': False,
                    'log.access_file': '/tmp/cherry_access.log',
                    'log.error_file': '/tmp/cherry_error.log'
                })
        app = cherrypy.tree.mount(DotaStats())
        WSGIServer(app).run()
    else:
        if options.port:
            cherrypy.config.update( {'server.socket_port': int(options.port) } )
        cherrypy.quickstart(DotaStats(), '/', config=config)

