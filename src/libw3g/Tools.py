from cStringIO import StringIO
from struct import *
import string
import zlib

try:
    import betterprint as pprint
except:
    import pprint


pprint = pprint.pprint

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

        dump(rest)


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

def extractString(io, decode=True):
    _startpos = io.tell()
    b, c = [], io.read(1)
    while c and c!='\0':
        b.append(c)
        c = io.read(1)
    string = ''.join(b)

    if decode:
        return string.decode('utf8')
    else:
        return string

def extractPlayer(io):
    record_flag, player_id = extract("BB", io)
    name = extractString(io)
    io.read(2)
    return {'RecordFlag':record_flag, 'PlayerId':player_id, 'Name': name}

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

def formatGametime(milliseconds):
    #hours   = int(milliseconds/1000/60/60)
    minutes = int(milliseconds/1000/60)
    seconds = int(milliseconds/1000) - 60*minutes
    return "%2d:%02d" % (minutes, seconds)


def getEmptyGamestate():
    return { 'gametime': 0, 'debug': {} }
