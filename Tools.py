from cStringIO import StringIO
from struct import *
import string
import zlib

def dump(data):
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


# TODO: deprecate
def eof(io):
    pos = io.tell()
    if io.read(1)=='':
        return True
    else:
        io.seek(pos)
        return False

def skip(size, io):
    io.seek(io.tell()+size)

def extract(fmt, io):
    data = unpack(fmt, io.read(calcsize(fmt)))
    return data

def extractIO(size, io):
    return StringIO(io.read(size))

def extractString(io):
    _startpos = io.tell()
    b, c = [], io.read(1)
    while c and c!='\0':
        b.append(c)
        c = io.read(1)
    return ''.join(b)

def extractPlayer(io):
    record_id, player_id = extract("BB", io)
    name = extractString(io)
    io.read(2)
    return record_id, player_id, name

def decodeGameInfo(data):
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
