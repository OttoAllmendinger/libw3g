from GameBlockReader import GameBlockReader
from Tools import *

from logging import basicConfig, debug


class ReplayReader:
    def __init__(self, gamestate):
        self.state = gamestate
        self.gameBlockReader = GameBlockReader(self.state)

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

        ioGameinfo = decodeGameInfo(extractString(io, decode=False))
        b_speed, b_vis, b_teams, b_sharing = extract('bbbb9x', ioGameinfo)

        # TODO: convert these values properly

        gameinfo['speed'] = b_speed
        gameinfo['visibility'] = b_vis
        gameinfo['fixedTeams'] = b_teams
        gameinfo['unitSharing'] = b_sharing
        gameinfo['mapName']= extractString(ioGameinfo)
        gameinfo['gameHost'] = extractString(ioGameinfo)

        player_slots = extract('L', io)

        gameinfo['players'] = players = [self.state['host']]

        io.read(8)

        while True:
            _lastpos = io.tell()
            p = extractPlayer(io)
            io.read(4)
            if p[0] in [0x00, 0x16]:
                players.append(p)
            else:
                io.seek(_lastpos)
                break

        self.state['playerMap'] = playermap = {}
        for p_type, p_id, p_name in players:
            playermap[p_id] = {
                    'name': p_name,
                    'isHost' : p_type==0x00,
            }

        return gameinfo


    def extractSlotRecord(self, io):
        keys = 'id downloaded slotStatus computer team color race aiLevel handicap'
        return dict(zip(keys.split(), extract('9b', io)))

    def extractStartRecord(self, io):
        slots = []
        startrecord = {'slots': slots }
        record_id, n_bytes, n_slots = extract("<bhb", io)

        assert record_id==0x19

        for i in range(n_slots):
            slots.append(self.extractSlotRecord(io))

        playerMap = self.state['playerMap']

        for slot in slots:
            p_id = slot['id']
            if p_id in playerMap.keys():
                playerMap[p_id].update(slot)

        keys = "random_seed select_mode start_spots".split()
        startrecord.update(dict(zip(keys, extract("LBB", io))))


        return startrecord

    def parse(self, io):
        header = self.state['header'] = self.extractHeader(io)

        gameio = StringIO()
        for i in range(header['blocks']):
            c_size, u_size, checksum = extract("HHL", io)
            data = io.read(c_size)
            gameio.write(inflate(data[2:]))
        gameio.seek(4)

        self.state['host'] = extractPlayer(gameio)
        self.state['info'] = self.extractGameInfo(gameio)
        self.state['startrecord'] = self.extractStartRecord(gameio)
        self.gameBlockReader.parse(gameio)
