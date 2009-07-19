from cStringIO import StringIO

from tools import *
from struct import *

import logging

logging.basicConfig(level=1)

def StaticRead(size):
    if type(size)==str:
        size = calcsize(size)
    return lambda block, fp: read(fp, size)

def StringRead():
    return lambda block, fp: extract_string(fp)

class DataBlock:
    def __init__(self, blockId, name):
        self.blockId = blockId
        self.name = name

    def __str__(self):
        return '<Block 0x%02X %s>' % (self.blockId, self.name)

class BlockReader:
    def __init__(self):
        self.blockMap = {}

    def define(self, blockId, blockName, callback=None):
        if callback==None:
            callback = getattr(self, blockName)
        self.blockMap[blockId] = DataBlock(blockId, blockName), callback

    def defineRange(self, firstBlock, lastBlock, blockName, callback=None):
        for _id in range(firstBlock, lastBlock+1):
            self.define(_id, blockName, callback)

    def parse(self, fp):
        while not eof(fp):
            _id, = extract(fp, 'B')
            if _id not in self.blockMap.keys():
                raise Exception("Undefined Block 0x%02X" % _id)
            block, callback = self.blockMap[_id]
            #logging.debug('parse block %s' % block)
            callback(block, fp)

