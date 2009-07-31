import sys
from os.path import *

import time

import cgi
import cgitb
cgitb.enable()

print 'Content-Type: text/html'
print

form = cgi.FieldStorage()

fileitem = form['replayfile']
timestamp = int(form.getfirst('timestamp'))
outfilename = 'replay-upload/replay-%s.w3g' % timestamp
outfile = file(outfilename, 'w')
blocksize = 1024 * 4
downloaded = 0
buf = True
while buf:
    buf = fileitem.file.read(blocksize)
    outfile.write(buf)
    downloaded += len(buf)
    sys.stdout.write('%08d'%downloaded)
    sys.stdout.flush()
