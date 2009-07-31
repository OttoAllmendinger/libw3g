from os.path import *

import cgi
import cgitb
cgitb.enable()

#import parseDota


UPLOAD_DIR = 'replay-upload'

print 'Content-Type: text/html'
print

form = cgi.FieldStorage()

page = form.getfirst('p')

if page=='upload':
    print '<form action="upload.py" method="post" enctype="multipart/form-data">'
    print '<input type="file" name="replayfile">'
    print '<input type="hidden" name="timestamp" value="0">'
    print '<input type="hidden" name="bytes" value="1000000">'
    print '<input type="submit">'
    print '</form>'

elif page=='submit':
    fileitem = form['replayfile']
    size = int(form.getfirst('bytes'))
    ts = int(form.getfirst('timestamp'))
    outfilename = 'replay-upload/replay-%s.w3g' % ts
    outfile = file(outfilename, 'w')
    blocksize = 1024 * 8
    downloaded = 0
    buf = True
    while buf:
        buf = fileitem.file.read(blocksize)
        outfile.write(buf)
        downloaded += blocksize
        print '%s' % downloaded
