import os
import sys
import time
import json
import logging
from zipfile import ZipFile
from os.path import abspath, dirname, exists, join
from cStringIO import StringIO
from datetime import datetime

import cherrypy
from cherrypy import expose
from genshi.template import TemplateLoader

from libw3g import get_replay_id
import libw3g
import libw3g.Tools
import libdota.DotaParser
import libdota.DotaUnits

from dotastats import util
from dotastats.ReplayDB import ReplayDB
from dotastats.PlayerDB import PlayerDB

# TODO: maybe add http://www.thomasfrank.se/json_editor.html

loader = TemplateLoader(join(dirname(__file__), 'html'), auto_reload=True)

VALID_RU_VERSIONS = ('0.1', )


class DotaStats:
    @expose
    def set_admin(self):
        cherrypy.response.cookie['dotastats-admin'] = 'True'
        return 'cookie data was: %s' % cherrypy.request.cookie

    @expose
    def unset_admin(self):
        cherrypy.response.cookie['dotastats-admin'] = 'False'
        return 'cookie unset'

    def is_admin(self):
        return cherrypy.request.cookie.get('dotastats-admin')=='True'

    @expose
    def exists(self, replay_id):
        return unicode(util.replay_exists(replay_id))

    @expose
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

        metadata = {
            'file_timestamp': int(timestamp),
            'upload_timestamp': int(time.time()),
            'uploader_ip': cherrypy.request.remote.ip }

        util.add_replay(data, metadata)

    upload._cp_config = {'response.stream': True}

    @expose
    def submit(self, zipfile=None, debug=False):
        if zipfile==None:
            return loader.load("upload.tpl.html").generate(
                debug=debug).render("html")
        else:
            zipobj = ZipFile(StringIO(zipfile.file.read()))
            for info in zipobj.infolist():
                if info.filename.endswith("w3g"):
                    data = zipobj.open(info).read()
                    timestamp = time.mktime(
                            datetime(*info.date_time).timetuple())
                    metadata = {
                        'file_timestamp': int(timestamp),
                        'upload_timestamp': int(time.time()),
                        'uploader_ip': cherrypy.request.remote.ip }
                    util.add_replay(data, metadata)
            return 'great success'

    @expose
    def check_ru(self, version=None):
        if version in VALID_RU_VERSIONS:
            return str(True)
        else:
            return str(False)

    @expose
    def rebuild(self, targets='replay+gameinfo'):
        targets = targets.split("+")

    @expose
    def json(self, key, **k):
        if key=='gamedata':
            return json.dumps(dict((r.replay_id, r.gamedata)
                for r in util.get_replays()))
        elif key=='metadata':
            return json.dumps(
                    dict((r.replay_id, r.metadata) for r in
                        util.get_replays()))
        elif key=='players':
            return json.dumps(dict((p_name, p_data) for p_name, p_data in
                    util.get_players().items()))
        else:
            return '{}'

    @expose
    def test(self):
        return loader.load('test.tpl.html').generate().render('html')


    @expose
    def game(self, replay_id, debug=False):
        replay = next(r for r in util.get_replays() if r.replay_id==replay_id)
        return loader.load("gamedetails.tpl.html").generate(
                replay=replay, debug=debug).render("html")

    @expose
    def index(self, debug=False):
        return loader.load('listview.tpl.html').generate(
                replays=util.get_replays(), debug=debug).render('html')

    @expose
    def highscore(self, debug=False):
        return loader.load("highscore.tpl.html").generate(
                debug=debug).render('html')

    @expose
    def static(self):
        return "you shouldn't see this"


if __name__=='__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-p', '--port')
    parser.add_option('--fastcgi', action='store_true')
    parser.add_option('--replaydb')
    #parser.add_option('--playerdb')
    options, args = parser.parse_args()

    config = {
        '/': {
            'tools.gzip.on': True,
            'tools.encode.on': True,
            'tools.encode.encoding': 'utf8',
            'tools.encode.add_charset': True,
            'tools.staticdir.root': join(dirname(abspath(__file__)))},
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static' }}

    dotastats = DotaStats()

    if options.fastcgi:
        from flup.server.fcgi import WSGIServer
        cherrypy.config.update( {
                    'engine.autoreload_on': False,
                    'tools.sessions.on': True,
                    'log.screen': False,
                    'log.access_file': '/tmp/cherry_access.log',
                    'log.error_file': '/tmp/cherry_error.log'
                })
        app = cherrypy.tree.mount(dotastats)
        WSGIServer(app).run()
    else:
        if options.port:
            cherrypy.config.update( {'server.socket_port': int(options.port) } )
        cherrypy.quickstart(dotastats, '/', config=config)

