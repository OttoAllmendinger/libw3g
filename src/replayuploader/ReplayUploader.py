import os
import sys
import urllib2
import hashlib
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
                self.cgiurl+'/replay/exists/%s' % rphash).read().strip()

        if response=='False':
            return False
        else:
            return True

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
    rpfile = sys.argv[1]
    uploader = ReplayUploader('http://localhost:8080/')

    #if uploader.exists(rpfile):
        #print 'replay already exists'
    #else:
    uploader.upload(rpfile)
