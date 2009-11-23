from Tools import *

def dumpGameIO(gameIo):
    pos = gameIO.tell()
    file('gameIO.dat', 'w').write(gameIO.read())
    gameIO.seek(pos)

def dumpTimeSlot(tsIo):
    pos = tsIo.tell()
    dump(tsIo.read(32))
    tsIo.seek(pos)
