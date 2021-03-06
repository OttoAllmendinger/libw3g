
from logging import basicConfig, debug

from GameBlockReader import GameBlockReader
from Tools import *
from util import get_replay_id


class ReplayReader:
    def __init__(self, gamestate):
        self.state = gamestate
        self.gameBlockReader = GameBlockReader(self.state)

    def extractHeader(self, io):
        keys = 'intro size c_size version u_size blocks'.split()
        header = dict(zip(keys, extract('26s2xIIIII', io)))
        assert header['version']==1
        keys = 'ident major_v build_v flags length checksum'.split()
        header.update(dict(zip(keys, extract('4sIHHII', io))))
        header['ident'] = header['ident'][::-1]
        io.seek(header['size'])
        return header

    def parseGameInfo(self, io):
        self.state['info'] = gameinfo = {}
        gameinfo['name'] = extractString(io)
        io.read(1)

        ioGameinfo = decodeGameInfo(extractString(io, decode=False))
        b_speed, b_vis, b_teams, b_sharing = extract('bbbb9x', ioGameinfo)

        # TODO: convert these values properly

        gameinfo['speed'] = b_speed
        gameinfo['visibility'] = b_vis
        gameinfo['fixed_teams'] = b_teams
        gameinfo['unit_sharing'] = b_sharing
        gameinfo['map_name']= extractString(ioGameinfo)
        gameinfo['game_host'] = extractString(ioGameinfo)

        player_slots = extract('I', io)

        records = [self.state['host']]

        io.read(8)

        rid = 1

        while True:
            _lastpos = io.tell()
            p = extractPlayer(io)
            io.read(4)
            if p['record_flag'] in [0x00, 0x16]:
                records.append(p)
            else:
                io.seek(_lastpos)
                break


        self.state['players'] = players = {}
        for rid, rec in enumerate(records):
            players[rec['player_id']] = rec
            rec['is_admin']= (rid==0)

        return gameinfo


    def extractSlotRecord(self, io):
        keys = ('player_id downloaded slot_status computer '
                'team color race ai_level handicap')
        return dict(zip(keys.split(), extract('9b', io)))

    def parseStartRecord(self, io):
        startrecord = {}
        record_id, n_bytes, n_slots = extract("<bhb", io)

        assert record_id==0x19

        for i in range(n_slots):
            sid = i+1
            slot_data = self.extractSlotRecord(io)
            if slot_data['slot_status'] != 0:
                pid = slot_data['player_id']
                if not pid in self.state['players']:
                    continue
                player = self.state['players'][pid]
                player['slot_id']=sid
                player.update(slot_data)

        keys = "random_seed select_mode start_spots".split()
        startrecord.update(dict(zip(keys, extract("IBB", io))))

        return startrecord

    def parse(self, io):
        self.state['replay_id'] = get_replay_id(io.read())
        io.seek(0)
        header = self.state['header'] = self.extractHeader(io)

        gameio = StringIO()
        for i in range(header['blocks']):
            c_size, u_size, checksum = extract("HHI", io)
            data = io.read(c_size)
            gameio.write(inflate(data[2:]))
        gameio.seek(4)

        self.state['host'] = extractPlayer(gameio)
        self.parseGameInfo(gameio)
        self.parseStartRecord(gameio)
        self.gameBlockReader.parse(gameio)
