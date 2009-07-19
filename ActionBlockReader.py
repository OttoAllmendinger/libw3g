from BlockReader import *

class ActionBlockReader(BlockReader):
    def __init__(self):
        BlockReader.__init__(self)

        self.define(0x01, 'Pause',              StaticRead(0))
        self.define(0x02, 'Resume',             StaticRead(0))
        self.define(0x03, 'SetSpeed',           StaticRead(1))
        self.define(0x04, 'IncreaseSpeed',      StaticRead(0))
        self.define(0x05, 'DecreaseSpeed',      StaticRead(0))
        self.define(0x06, 'SaveGame')
        self.define(0x07, 'SaveGameDone',       StaticRead('H'))
        self.defineRange(0x10, 0x14, 'UseAbility')
        self.define(0x16, 'ChangeSelection')
        self.define(0x17, 'AssingGroupHotkey')
        self.define(0x18, 'SelectGroupHotkey',  StaticRead('BB'))
        self.define(0x19, 'SelectSubgroup',     StaticRead('LLL'))
        self.define(0x1A, 'UpdateSubgroup',     StaticRead(0))
        self.define(0x1B, 'Unknown',            StaticRead('<BLL'))
        self.define(0x1C, 'SelectGroundItem',   StaticRead('<BLL'))
        self.define(0x1D, 'CancelHeroRevival',  StaticRead('<LL'))
        self.define(0x1E, 'RemoveFromQueue',    StaticRead('<BL'))
        self.defineRange(0x20, 0x32, 'EnterCheat')
        self.define(0x50, 'ChangeAllys')
        self.define(0x51, 'TransferResources',  StaticRead('<BLL'))
        self.define(0x60, 'ChatTrigger')
        self.define(0x61, 'EscapePressed',      StaticRead(0))
        self.define(0x62, 'ScenarioTrigger',    StaticRead('LLL'))
        self.define(0x66, 'SelectHeroSkill',    StaticRead(0))
        self.define(0x67, 'ChooseBuilding',     StaticRead(0))
        self.define(0x68, 'MinimapSignal',      StaticRead('fff'))
        self.define(0x69, 'ContinueGame',       StaticRead(16))
        self.define(0x6A, 'ContinueGame',       StaticRead(16))
        self.define(0x6A, 'Unknown',            StaticRead('B'))


    def SaveGame(self, block, fp):
        name = extract_string(fp)
        self.game['SaveGames'].append({'name': name})

    def ChatTrigger(self, block, fp):
        extract(fp, 'LL')
        message = extract_string(fp)

    def AssingGroupHotkey(self, block, fp):
        group, n_units = extract(fp, '<BH')
        read(fp, 8*n_units)

    def ChangeSelection(self, block, fp):
        select_mode, n_units = extract(fp, '<BH')
        read(fp, 8*n_units)

    def ChangeAllys(self, block, fp):
        slot, flag = extract(fp, '<BL')

    def UseAbility(self, block, fp):
        sizes = {
            0x10: '<H3L',
            0x11: '<H5L',
            0x12: '<H7L',
            0x13: '<H9L',
            0x14: '<H5L9x3L'
        }
        extract(fp, sizes[block.blockId])

    def EnterCheat(self, block, fp):
        pass
