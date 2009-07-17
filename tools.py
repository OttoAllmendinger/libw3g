from cStringIO import StringIO
#from array import array
from struct import *
import string
import zlib


def dump(data, mode=''):
    MAXLINE = 16
    valid_chars = string.letters + string.digits + string.punctuation + ' '
    linec=0
    mode_hex = 'h' in mode
    mode_col = 'c' in mode

    if mode_col:
        print '|'.join("%4d" % i for i in range(MAXLINE))

    for char in data:
        linec += 1
        if not mode_hex and char in valid_chars:
            print ".  %s" % char,
        else:
            print "0x%02X" % (ord(char)),
        if linec>MAXLINE:
            print
            linec=0
    print


def read(fp, size, seek=True):
    pos = fp.tell()
    data = fp.read(size)
    if not seek:
        fp.seek(pos)
    return data

def extract(fp, fmt, seek=True):
    data = unpack(fmt, read(fp, calcsize(fmt), seek))
    return data

def extract_string(fp, seek=True):
    _startpos = fp.tell()
    b, c = [], read(fp, 1)
    while c and c!='\0':
        b.append(c)
        c = read(fp, 1)
    if not seek:
        fp.seek(_startpos)
    return ''.join(b)

def decode_gameinfo(data):
    enc = map(ord, data)
    tmp = ''
    mask=0
    for i in range(len(enc)):
        if i%8==0:
            mask = enc[i]
        else:
            tmp += chr(enc[i]-int((mask&(1<<(i%8)))==0))
    return StringIO(tmp)

def inflate(data):
    dc = zlib.decompressobj(-zlib.MAX_WBITS)
    inf = dc.decompress(data)
    inf += dc.flush()
    return inf
