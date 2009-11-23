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
        gameinfo['Name'] = extractString(io)
        io.read(1)

        ioGameinfo = decodeGameInfo(extractString(io, decode=False))
        b_speed, b_vis, b_teams, b_sharing = extract('bbbb9x', ioGameinfo)

        # TODO: convert these values properly

        gameinfo['Speed'] = b_speed
        gameinfo['Visibility'] = b_vis
        gameinfo['FixedTeams'] = b_teams
        gameinfo['UnitSharing'] = b_sharing
        gameinfo['MapName']= extractString(ioGameinfo)
        gameinfo['GameHost'] = extractString(ioGameinfo)

        player_slots = extract('L', io)

        records = [self.state['Host']]

        io.read(8)

        rid = 1

        while True:
            _lastpos = io.tell()
            p = extractPlayer(io)
            io.read(4)
            if p['RecordFlag'] in [0x00, 0x16]:
                records.append(p)
            else:
                io.seek(_lastpos)
                break


        gameinfo['Players'] = players = {}
        for rid, rec in enumerate(records):
            players[rec['PlayerId']] = rec
            rec['IsAdmin']= (rid==0)

        return gameinfo


    def extractSlotRecord(self, io):
        keys = ('PlayerId Downloaded SlotStatus Computer '
                'Team Color Race AiLevel Handicap')
        return dict(zip(keys.split(), extract('9b', io)))

    def extractStartRecord(self, io):
        slots = {}
        startrecord = {'Slots': slots }
        record_id, n_bytes, n_slots = extract("<bhb", io)

        self.state['Slots'] = {}

        assert record_id==0x19

        for i in range(n_slots):
            sid = i+1
            slot = self.extractSlotRecord(io)
            if slot['SlotStatus'] != 0:
                pid = slot['PlayerId']
                player = self.state['Players'][pid]
                player['SlotId']=sid
                self.state['Slots'][sid] = player

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

        self.state['Host'] = extractPlayer(gameio)
        self.state['Info'] = self.extractGameInfo(gameio)
        self.state['Players'] = self.state['Info']['Players']
        self.state['StartRecord'] = self.extractStartRecord(gameio)
        self.gameBlockReader.parse(gameio)
