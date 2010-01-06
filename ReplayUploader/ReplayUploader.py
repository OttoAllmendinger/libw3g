import os
import sys
import urllib2
import hashlib
import optparse
import time

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

register_openers()


import libw3g


VERSION = '0.1'

def console_output(n_bytes):
    print n_bytes

class ReplayUploader:
    def __init__(self, cgiurl):
        self.cgiurl = cgiurl

    def exists(self, path):
        replay_id = libw3g.get_replay_id(file(path, 'rb').read())
        response = urllib2.urlopen(
                self.cgiurl+'/exists/%s' % replay_id).read().strip()
        return str(response)=='True'

    def upload(self, path, callback=console_output):
        datagen, headers = multipart_encode({
                'replay_file': file(path, 'rb'),
                'timestamp': str(libw3g.get_timestamp(path))
        })

        request = urllib2.Request(self.cgiurl+'/upload', datagen, headers)
        buf = urllib2.urlopen(request)

        while True:
            data = buf.read(8)
            if data=='-'*8:
                break
            else:
                downloaded = int(data)
                callback(downloaded)
        print buf.read()

def test_host(host):
    url = 'http://%s/check_ru?version=%s' % (host, VERSION)
    response = urllib2.urlopen(url).read()

    if response=='True':
        return True
    else:
        raise Exception('Invalid ReplayUploader version, please update\n'
                        'http://code.google.com/p/libw3g/')


def wait_for_change(path):
    timestamp = current_ts = libw3g.get_timestamp(path)
    while (timestamp==current_ts):
        current_ts = libw3g.get_timestamp(path)
        time.sleep(1)

if __name__=='__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option("-H", "--host")
    #option_parser.add_option("-w", "--watch", action='store_true')
    (options, args) = option_parser.parse_args()

    host = options.host
    replay_files = args[:]

    uploader = ReplayUploader('http://' + host)

    for replay_file in replay_files:
        if uploader.exists(replay_file):
            print 'replay already exists'
        else:
            uploader.upload(replay_file)
