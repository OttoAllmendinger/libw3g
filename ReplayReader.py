from GameBlockReader import GameBlockReader
from Tools import *

from logging import basicConfig, debug


class ReplayReader:
    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.gameBlockReader = GameBlockReader(self.gamestate)

    def extractHeader(self, io):
        keys = 'intro size c_size version u_size blocks'.split()
        header = dict(zip(keys, extract('26s2xLLLLL', io)))
        assert header['version']==1
        keys = 'ident major_v build_v flags length checksum'.split()
        header.update(dict(zip(keys, extract('4sLHHLL', io))))
        header['ident'] = header['ident'][::-1]
        io.seek(header['size'])
        return header

    def extractGameInfo(self, io):
        gameinfo = {}
        gameinfo['name'] = extractString(io)
        io.read(1)

        ioGameinfo = decodeGameInfo(extractString(io))
        b_speed, b_vis, b_teams, b_sharing = extract('bbbb9x', ioGameinfo)

        # TODO: convert these values properly

        gameinfo['speed'] = b_speed
        gameinfo['visibility'] = b_vis
        gameinfo['fixed_teams'] = b_teams
        gameinfo['unit_sharing'] = b_sharing
        gameinfo['map_name']= extractString(ioGameinfo)
        gameinfo['game_host'] = extractString(ioGameinfo)

        player_slots = extract('L', io)

        gameinfo['players'] = []

        io.read(8)

        while True:
            _lastpos = io.tell()
            p = extractPlayer(io)
            io.read(4)
            if p[0] in [0x00, 0x16]:
                gameinfo['players'].append(p)
            else:
                io.seek(_lastpos)
                break

        return gameinfo


    def extractSlotRecord(self, io):
        keys = 'id downloaded slotstatus computer team color race ai_level handicap'
        return dict(zip(keys.split(), extract('9b', io)))

    def extractStartRecord(self, io):
        startrecord = {'slots': [] }
        record_id, n_bytes, n_slots = extract("<bhb", io)

        assert record_id==0x19

        for i in range(n_slots):
            startrecord['slots'].append(self.extractSlotRecord(io))

        keys = "random_seed select_mode start_spots".split()
        startrecord.update(dict(zip(keys, extract("LBB", io))))

        return startrecord

    def parse(self, io):
        header = self.gamestate['header'] = self.extractHeader(io)

        gameio = StringIO()
        for i in range(header['blocks']):
            c_size, u_size, checksum = extract("HHL", io)
            data = io.read(c_size)
            gameio.write(inflate(data[2:]))
        gameio.seek(4)

        self.gamestate['host'] = extractPlayer(gameio)
        self.gamestate['info'] = self.extractGameInfo(gameio)
        self.gamestate['startrecord'] = self.extractStartRecord(gameio)
        self.gameBlockReader.parse(gameio)
