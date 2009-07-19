from GameBlockReader import GameBlockReader

from tools import *

class ReplayReader:
    def __init__(self):
        self.gameBlockReader = GameBlockReader()

    def extractHeader(self, fp):
        keys = 'intro size c_size version u_size blocks'.split()
        header = dict(zip(keys, extract(fp, '28sLLLLL')))
        assert header['version']==1
        keys = 'ident major_v build_v flags length checksum'.split()
        header.update(dict(zip(keys, extract(fp, '4sLHHLL'))))
        header['ident'] = header['ident'][::-1]
        fp.seek(header['size'])
        return header

    def extractGameInfo(self, fp):
        gameinfo = {}
        gameinfo['name'] = extract_string(fp)
        fp.read(1)

        fpgameinfo = decode_gameinfo(extract_string(fp))
        b_speed, b_vis, b_teams, b_sharing = extract(fpgameinfo, 'bbbb9x')

        # TODO: convert these values properly

        gameinfo['speed'] = b_speed
        gameinfo['visibility'] = b_vis
        gameinfo['fixed_teams'] = b_teams
        gameinfo['unit_sharing'] = b_sharing
        gameinfo['map_name']= extract_string(fpgameinfo)
        gameinfo['game_host'] = extract_string(fpgameinfo)

        player_slots = extract(fp, 'L')

        gameinfo['players'] = []

        read(fp, 8)

        while True:
            _lastpos = fp.tell()
            p = extract_player(fp)
            _info = fp.read(4)
            if p[0] in [0x00, 0x16]:
                gameinfo['players'].append(p)
            else:
                fp.seek(_lastpos)
                break

        return gameinfo


    def extractSlotRecord(self, fp):
        keys = 'id downloaded slotstatus computer team color race ai_level handicap'
        return dict(zip(keys.split(), extract(fp, '9b')))

    def extractStartRecord(self, fp):
        startrecord = {'slots':[]}
        record_id, n_bytes, n_slots = extract(fp, "<bhb")

        assert record_id==0x19

        for i in range(n_slots):
            startrecord['slots'].append(self.extractSlotRecord(fp))

        keys = "random_seed select_mode start_spots".split()
        startrecord.update(dict(zip(keys, extract(fp, "LBB"))))

        return startrecord

    def parse(self, fp):
        game = {}
        header = self.extractHeader(fp)
        game['header'] = header

        fpgame = StringIO()
        for i in range(header['blocks']):
            c_size, u_size, checksum = extract(fp, "HHL")
            data = fp.read(c_size)
            fpgame.write(inflate(data[2:]))
        fpgame.seek(4)

        game['host'] = extract_player(fpgame)
        game['info'] = self.extractGameInfo(fpgame)
        game['startrecord'] = self.extractStartRecord(fpgame)

        self.gameBlockReader.parse(fpgame)
