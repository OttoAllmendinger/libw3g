from cStringIO import StringIO
#from array import array
from struct import *
import string
import zlib

def dumpline(data):
    if not data:
        return
    else:
        data, rest = data[:24], data[24:]

        valid_chars = string.letters + string.digits + string.punctuation + ' '

        hexdata = '|'.join("%02X" % ord(c) for c in data)
        ascdata = '|'.join((("%-2s" % c) if c in valid_chars else "  ") for c in data)

        print hexdata
        print ascdata

        dumpline(rest)



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


def read(fp, size):
    data = fp.read(size)
    return data

def eof(fp):
    pos = fp.tell()
    if fp.read(1)=='':
        return True
    else:
        fp.seek(pos)
        return False

def extract(fp, fmt):
    data = unpack(fmt, read(fp, calcsize(fmt)))
    return data

def extract_fp(fp, size):
    return StringIO(fp.read(size))

def extract_string(fp):
    _startpos = fp.tell()
    b, c = [], read(fp, 1)
    while c and c!='\0':
        b.append(c)
        c = read(fp, 1)
    return ''.join(b)

def extract_player(fp):
    record_id, player_id = extract(fp, "BB")
    name = extract_string(fp)
    fp.read(2)
    return record_id, player_id, name

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
