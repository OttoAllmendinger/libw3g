from StringIO import StringIO

from logging import basicConfig, debug, warn
from pprint import pprint

from tools import *

basicConfig(level=0)

#  word = 2 bytes   'h' 
# dword = 4 bytes   'L'

class UnknownBlockException:
    pass

def get_header(fp):
    keys = 'intro size c_size version u_size blocks'.split()
    header = dict(zip(keys, extract(fp, '28sLLLLL')))
    if header['version']==1:
        keys = 'ident major_v build_v flags length checksum'.split()
        header.update(dict(zip(keys, extract(fp, '4sLHHLL'))))
        header['ident'] = header['ident'][::-1]
    return header

def get_game_data(header, fp):
    fp.seek(header['size'])
    buf = StringIO()
    for i in range(header['blocks']):
        c_size, u_size, checksum = extract(fp, "HHL")
        data = fp.read(c_size)
        buf.write(inflate(data[2:]))
    buf.flush()
    buf.seek(0)
    return buf


def get_player(fp):
    record_id, player_id = extract(fp, "BB")
    name = extract_string(fp)

    fp.read(2)

    return record_id, player_id, name

def get_gameinfo(fp):
    game_name = extract_string(fp)
    debug("game_name=%s" % game_name)
    fp.read(1)
    fp_gi = decode_gameinfo(extract_string(fp))
    b_speed, b_vis, b_teams, b_sharing = extract(fp_gi, 'bbbb9x')

    gi = {}

    # TODO: convert these values properly

    gi['speed'] = b_speed
    gi['visibility'] = b_vis
    gi['fixed_teams'] = b_teams
    gi['unit_sharing'] = b_sharing
    gi['map_name']= extract_string(fp_gi)
    gi['game_host'] = extract_string(fp_gi)

    player_slots = extract(fp, 'L')

    gi['players'] = []

    read(fp, 8)

    while True:
        _lastpos = fp.tell()
        p = get_player(fp)
        _info = fp.read(4)
        #dump(_info, 'h')
        if p[0] in [0x00, 0x16]:
            gi['players'].append(p)
        else:
            fp.seek(_lastpos)
            break

    return gi

def get_slotrecord(fp):
    keys = 'id downloaded slotstatus computer team color race ai_level handicap'
    return dict(zip(keys.split(), extract(fp, '9b')))


def get_gamestartrecord(fp):
    gsr = {'slots':[]}
    record_id, n_bytes, n_slots = extract(fp, "<bhb")

    assert record_id==0x19

    for i in range(n_slots):
        gsr['slots'].append(get_slotrecord(fp))

    keys = "random_seed select_mode start_spots".split()
    gsr.update(dict(zip(keys, extract(fp, "LBB"))))

    return gsr

def parse_first_block(fp):
    read(fp, 4)
    player = get_player(fp)
    game = get_gameinfo(fp)
    gsr = get_gamestartrecord(fp)
    pprint(gsr)

def parse_leave(fp):
    data = extract(fp, "<LBLL")
    reason, player_id, result, unknown = data
    print map(hex, data)

def parse_action(fp):
    _id, = extract(fp, 'b')
    if _id==0x01:
        # pause
        pass
    elif _id==0x02:
        # resume
        pass
    elif _id==0x03:
        # set speed
        new_speed = extract(fp, 'b')[0]
    elif _id==0x04:
        # increase speed
        pass
    elif _id==0x05:
        # decrease speed
        pass
    elif _id==0x06:
        # save game
        savegame_name = extract_string(fp)
    elif _id==0x07:
        # save game finished
        status = extract(fp, 'H')
    elif _id==0x10:
        # unit/building ability
        data = extract(fp, '<H3L')
    elif _id==0x11:
        data = extract(fp, '<H5L')
    elif _id==0x12:
        data = extract(fp, '<H7L')
    elif _id==0x13:
        data = extract(fp, '<H9L')
    elif _id==0x14:
        data = extract(fp, '<H5L9x2L')
    else:
        print 'unknown action_id 0x%02X' % _id

def parse_timeslot(fp):
    n_bytes, time_increment = extract(fp, 'HH')
    fp_ts = StringIO(read(fp, n_bytes-2))
    player_id, block_length = extract(fp, '<bh')
    for i in range(block_length):
        parse_action(fp_ts)


def parse_chatmessage(fp):
    data = extract(fp, "<bhbl")
    sender, n_bytes, flags, mode = data
    msg = extract_string(fp)

def parse_block(fp):
    data = read(fp, 8, False)
    _id, = extract(fp, 'B')
    if _id in (0x1A, 0x1B, 0x1C): # start fps
        read(fp, 4)
    elif _id==0x17:
        parse_leave(fp)
    elif _id==0x1F: # timeslot fp
        parse_timeslot(fp)
    elif _id==0x20: # chat message
        parse_chatmessage(fp)
    elif _id==0x22: # unkown
        read(fp, 5)
    elif _id==0x23: # unknown
        read(fp, 10)
    elif _id==0x2F: # forced end game countdown
        read(fp, 8)
    elif _id==0x00:
        print ' --- finished --- '
        fp.read()
    else: # failure
        print "Unknown blockid %02X" % _id
        dump(data, 'h')
        rest = fp.read()
        print "%d bytes left" % len(rest)
        raise UnknownBlockException()

    #dump(read(fp, 256, False))

def get_replay(fp):
    header = get_header(fp)
    debug("header=%s" % header)

    game_data = get_game_data(header, fp)
    read(game_data, 4)
    player = get_player(game_data)
    game = get_gameinfo(game_data)
    gsr = get_gamestartrecord(game_data)
    #pprint(gsr)

    while read(game_data, 1, seek=False):
        parse_block(game_data)


def usage(name):
    print "Usage: %s REPLAY-FILE" % name

if __name__=="__main__":
    import sys
    if len(sys.argv)>1:
        f = sys.argv[1]
        get_replay(file(f))
    else:
        usage(sys.argv[0])

