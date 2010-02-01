from BlockReader import *

class ActionBlockReader(BlockReader):
    def __init__(self, gamestate):
        BlockReader.__init__(self, gamestate)

        self.define(0x01, 'Pause',              Skip(0))
        self.define(0x02, 'Resume',             Skip(0))
        self.define(0x03, 'SetSpeed',           Skip(1))
        self.define(0x04, 'IncreaseSpeed',      Skip(0))
        self.define(0x05, 'DecreaseSpeed',      Skip(0))
        self.define(0x06, 'SaveGame')
        self.define(0x07, 'SaveGameDone',       Skip('I'))
        self.defineRange(0x10, 0x14, 'UseAbility')
        self.define(0x16, 'ChangeSelection')
        self.define(0x17, 'AssingGroupHotkey')
        self.define(0x18, 'SelectGroupHotkey',  Skip('BB'))
        self.define(0x19, 'SelectSubgroup',     Skip('III'))
        self.define(0x1A, 'UpdateSubgroup',     Skip(0))
        self.define(0x1B, 'Unknown',            Skip('BII'))
        self.define(0x1C, 'SelectGroundItem',   Skip('BII'))
        self.define(0x1D, 'CancelHeroRevival',  Skip('II'))
        self.define(0x1E, 'RemoveFromQueue',    Skip('BI'))
        self.defineRange(0x20, 0x32, 'EnterCheat')
        self.define(0x50, 'ChangeAllys')
        self.define(0x51, 'TransferResources',  Skip('BII'))
        self.define(0x60, 'ChatTrigger')
        self.define(0x61, 'EscapePressed',      Skip(0))
        self.define(0x62, 'ScenarioTrigger',    Skip('III'))
        self.define(0x66, 'SelectHeroSkill',    Skip(0))
        self.define(0x67, 'ChooseBuilding',     Skip(0))
        self.define(0x68, 'MinimapSignal',      Skip('fff'))
        self.define(0x69, 'ContinueGame',       Skip(16))
        self.define(0x6A, 'ContinueGame',       Skip(16))
        self.define(0x6A, 'Unknown',            Skip('B'))

        self.currentPlayer = None

    def handleSaveGame(self, block, io):
        name = extractString(io)

    def handleChatTrigger(self, block, io):
        extract('II', io)
        message = extractString(io)

    def handleAssingGroupHotkey(self, block, io):
        group, n_units = extract('BH', io)
        io.read(8*n_units)

    def handleChangeSelection(self, block, io):
        select_mode, n_units = extract('BH', io)
        io.read(8*n_units)

    def handleChangeAllys(self, block, io):
        slot, flag = extract('BI', io)
        #print 'ChangeAllys (%d, %d)' % (slot, flag)

    def handleUseAbility(self, block, io):
        sizes = {
            0x10: 'H3I',
            0x11: 'H5I',
            0x12: 'H7I',
            0x13: 'H9I',
            0x14: 'H5I9x3I'
        }
        extract(sizes[block.blockId], io)

    def handleEnterCheat(self, block, io):
        # TODO
        pass
