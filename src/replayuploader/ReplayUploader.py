import os
import sys
import urllib2
import hashlib
import optparse
import time

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


register_openers()



def console_output(n_bytes):
    print n_bytes

class ReplayUploader:
    def __init__(self, cgiurl):
        self.cgiurl = cgiurl

    def exists(self, path):
        rphash = hashlib.md5(file(path).read()).hexdigest()
        response = urllib2.urlopen(
                self.cgiurl+'exists/%s' % rphash).read().strip()

        return response=='True'

    def upload(self, path, callback=console_output):
        stat = os.stat(path)
        datagen, headers = multipart_encode({
                'replay_file': file(path, 'rb'),
                'timestamp': str(int(stat.st_ctime)),
        })

        request = urllib2.Request(self.cgiurl+'upload', datagen, headers)
        buf = urllib2.urlopen(request)

        while True:
            data = buf.read(8)
            if data=='-'*8:
                break
            else:
                downloaded = int(data)
                callback(downloaded)
        print buf.read()



if __name__=='__main__':
    option_parser = optparse.OptionParser()
    option_parser.add_option("-w", "--watch")
    (options, args) = option_parser.parse_args()
    cgi_url, replay_file = args

    uploader = ReplayUploader(cgi_url)

    while True:
        if uploader.exists(replay_file):
            print 'replay already exists'
        else:
            uploader.upload(replay_file)

        if options.watch:
            wait_for_change(replay_file)
        else:
            break
