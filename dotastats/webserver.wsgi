# vi:ft=python

import sys
import atexit

import cherrypy

sys.path.insert(0, '..')
from dotastats import webserver

ds_instance = webserver.DotaStats()

if cherrypy.engine.state==0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)
