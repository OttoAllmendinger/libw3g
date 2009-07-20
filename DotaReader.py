from ActionReader import ActionReader

from Tools import *

class DotaActionReader(ActionReader):
    def __init__(self, game):
        ActionReader.__init__(self, game)
        self.define(0x6B, 'DotaTrigger')

    def DotaTrigger(self, block, io):
        drx = extractString(io)
        a = extractString(io)
        b = extractString(io)
        c = extract('L', io)
