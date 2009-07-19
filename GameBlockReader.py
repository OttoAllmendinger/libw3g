from BlockReader import *
from ActionBlockReader import ActionBlockReader

class GameBlockReader(BlockReader):
    def __init__(self):
        BlockReader.__init__(self)

        self.actionBlockReader = ActionBlockReader()

        self.defineRange(0x1A, 0x1C, 'StartBlock', StaticRead(4))
        self.define(0x17, 'LeaveGame')
        self.defineRange(0x1E, 0x1F, 'TimeSlot')
        self.define(0x20, 'ChatMessage')
        self.define(0x22, 'Unknown', StaticRead(5))
        self.define(0x23, 'Unknown', StaticRead(10))
        self.define(0x2F, 'ForcedCountdown', StaticRead(8))
        self.define(0x00, 'Finish')

    def LeaveGame(self, block, fp):
        reason, player_id, result, unknown = extract(fp, '<LBLL')

    def ChatMessage(self, block, fp):
        sender, size, flags, mode = extract(fp, '<bhbl')
        message = extract_string(fp)

    def Finish(self, block, fp):
        fp.read()

    def TimeSlot(self, block, fp):
        n_bytes, time_inc = extract(fp, 'HH')
        fpcmd = extract_fp(fp, n_bytes-2)

        if not eof(fpcmd):
            player_id, block_length = extract(fpcmd, '<bH')
            fpaction = extract_fp(fpcmd, block_length)
            self.actionBlockReader.parse(fpaction)
