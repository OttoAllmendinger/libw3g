from ActionReader import ActionReader

from tools import *

class DotaActionReader(ActionReader):
    def __init__(self, game):
        ActionReader.__init__(self, game)
        self.define(0x6B, 'DotaTrigger')

    def DotaTrigger(self, block, fp):
        drx = extract_string(fp)
        a = extract_string(fp)
        b = extract_string(fp)
        c = extract(fp, 'L')
        #print locals()
