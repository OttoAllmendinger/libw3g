from os.path import *
import sys
import time
import shelve

import cgi
import cgitb
cgitb.enable()

import hashlib


print 'Content-Type: text/html'
print

form = cgi.FieldStorage()

action = form.getfirst('action')

upload_data = shelve.open("upload-data.db")

if action=='exists':
    filehash = form.getfirst('hash')
    print upload_data.get(filehash)!=None
elif action=='upload':
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
    outfile.close()
    infile = file(outfilename, 'r')
    filehash = hashlib.md5(infile.read()).hexdigest()
    upload_data[filehash]=timestamp
elif action=='dump':
    for k in upload_data.keys():
        print k, upload_data[k], '<br>'
