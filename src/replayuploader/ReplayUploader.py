import os
import sys
import urllib2
import hashlib


from MultipartPostHandler import MultipartPostHandler

def console_output(n_bytes):
    print n_bytes

class ReplayUploader:
    def __init__(self, cgiurl):
        self.cgiurl = cgiurl

    def exists(self, path):
        rphash = hashlib.md5(file(path).read()).hexdigest()
        response = urllib2.urlopen(
                self.cgiurl+'/upload.py?action=exists&hash=%s' % rphash).read().strip()

        if response=='False':
            return False
        else:
            return True

    def upload(self, path, callback=console_output):
        stat = os.stat(path)
        opener = urllib2.build_opener(MultipartPostHandler)
        params = {
                'replayfile': file(path, 'rb'),
                'timestamp': str(int(stat.st_ctime)),
        }

        buf = opener.open(self.cgiurl+'/upload.py?action=upload', params)

        while True:
            data = buf.read(8)
            if not data:
                break
            try:
                downloaded = int(data)
                callback(downloaded)
            except:
                print buf.read()
                raise


if __name__=='__main__':
    rpfile = sys.argv[1]
    uploader = ReplayUploader('http://localhost:8000/')

    if uploader.exists(rpfile):
        print 'replay already exists'
    else:
        uploader.upload(rpfile)
