from BlockReader import *
from ActionBlockReader import ActionBlockReader

from Tools import *
import Debug

class GameBlockReader(BlockReader):
    def __init__(self, gamestate):
        BlockReader.__init__(self, gamestate)

        self.actionBlockReader = ActionBlockReader(gamestate)

        self.defineRange(0x1A, 0x1C, 'StartBlock',  Skip(4))
        self.defineRange(0x1E, 0x1F, 'TimeSlot')

        self.define(0x22, 'RandomSeed',             Skip(5))
        self.define(0x23, 'Unknown',                Skip(10))
        self.define(0x2F, 'ForcedCountdown',        Skip(8))

        self.define(0x17, 'LeaveGame')
        self.define(0x20, 'ChatMessage')
        self.define(0x00, 'Finish')

    def handleLeaveGame(self, block, io):
        reason, player_id, result, unknown = extract('<LBLL', io)

    def handleChatMessage(self, block, io):
        sender, size, flags, mode = extract('<bhbl', io)
        message = extractString(io)

    def handleFinish(self, block, io):
        io.read()

    def handleTimeSlot(self, block, io):
        n_bytes, time_inc = extract('HH', io)
        cmdio = extractIO(n_bytes-2, io)

        self.state['gametime'] += time_inc

        while True:
            try:
                player_id, block_length = extract('<bH', cmdio)
                actionio = extractIO(block_length, cmdio)
            except ExtractionError:
                break
            self.actionBlockReader.currentPlayer = (
                        self.state['players'][player_id])
            self.actionBlockReader.parse(actionio)
