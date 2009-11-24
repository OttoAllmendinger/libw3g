import os
import sys
import urllib2
import hashlib
import optparse
import time

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


register_openers()


def get_timestamp(path):
    stat = os.stat(path)
    return int(stat.st_mtime)

def console_output(n_bytes):
    print n_bytes

class ReplayUploader:
    def __init__(self, cgiurl):
        self.cgiurl = cgiurl

    def exists(self, path):
        rphash = hashlib.md5(file(path).read()).hexdigest()
        response = urllib2.urlopen(
                self.cgiurl+'/exists/%s' % rphash).read().strip()

        return response=='True'

    def upload(self, path, callback=console_output):
        datagen, headers = multipart_encode({
                'replay_file': file(path, 'rb'),
                'timestamp': str(get_timestamp(path))
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

def wait_for_change(path):
    timestamp = current_ts = get_timestamp(path)
    while (timestamp==current_ts):
        current_ts = get_timestamp(path)
        time.sleep(1)

if __name__=='__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option("-w", "--watch", action='store_true')
    (options, args) = option_parser.parse_args()
    host, replay_file = args

    uploader = ReplayUploader('http://' + host)

    while True:
        if uploader.exists(replay_file):
            print 'replay already exists'
        else:
            uploader.upload(replay_file)

        if options.watch:
            wait_for_change(replay_file)
            print 'new replay found'
            time.sleep(1) # maybe warcraft needs time to write the replay
        else:
            break
