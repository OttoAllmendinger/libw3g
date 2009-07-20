from cStringIO import StringIO

from Tools import *
from struct import *

import struct

from logging import basicConfig, debug

basicConfig(level=1)

def Skip(size):
    if type(size)==str:
        size = calcsize(size)
    return lambda block, io: skip(size, io)

def StringRead():
    return lambda block, io: extractString(io)

class DataBlock:
    def __init__(self, blockId, name):
        self.blockId = blockId
        self.name = name

    def __str__(self):
        return '<Block 0x%02X %s>' % (self.blockId, self.name)

class BlockReader:
    def __init__(self, state):
        self.state = state
        self.blockMap = {}
        self.debug = False

    def define(self, blockId, blockName, callback=None):
        if callback==None:
            callback = getattr(self, 'handle'+blockName)
        self.blockMap[blockId] = DataBlock(blockId, blockName), callback

    def defineRange(self, firstBlock, lastBlock, blockName, callback=None):
        for _id in range(firstBlock, lastBlock+1):
            self.define(_id, blockName, callback)

    def parse(self, io):
        while True:
            try:
                _id, = extract('B', io)
            except struct.error:
                break

            if _id not in self.blockMap.keys():
                raise Exception("Undefined Block 0x%02X" % _id)

            block, callback = self.blockMap[_id]

            if self.debug and self.state['debug']['blockdebugger']:
                pos = io.tell()
                bdb = self.state['debug']['blockdebugger'](self, block, io)
                io.seek(pos)

            callback(block, io)
