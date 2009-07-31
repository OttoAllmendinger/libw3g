import os
import sys
import urllib2


from MultipartPostHandler import MultipartPostHandler

console_output = lambda x: sys.stdout.write(x+'\n')

def upload(url, rpfilename, callback=console_output):
    stat = os.stat(rpfilename)
    opener = urllib2.build_opener(MultipartPostHandler)
    params = {
            'replayfile': file(rpfilename, 'rb'),
            'timestamp': str(int(stat.st_ctime)),
    }

    buf = opener.open(url, params)

    while True:
        data = buf.read(8)
        if data:
            downloaded = int(data)
            callback(downloaded)
        else:
            break



