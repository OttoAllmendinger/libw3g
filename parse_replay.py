import psyco
psyco.full()

from cStringIO import StringIO

from logging import basicConfig, debug, warn
from pprint import pprint

from tools import *

basicConfig(level=0)

#  word = 2 bytes   'h' 
# dword = 4 bytes   'L'

class UnknownBlockException(Exception):
    pass

class UnknownActionException(Exception):
    pass

def get_header(fp):
    keys = 'intro size c_size version u_size blocks'.split()
    header = dict(zip(keys, extract(fp, '28sLLLLL')))
    if header['version']==1:
        keys = 'ident major_v build_v flags length checksum'.split()
        header.update(dict(zip(keys, extract(fp, '4sLHHLL'))))
        header['ident'] = header['ident'][::-1]
    return header

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

def parse_leave(game, fp):
    data = extract(fp, "<LBLL")
    reason, player_id, result, unknown = data
    #print map(hex, data)

def parse_action(game, fp):
    _id, = extract(fp, 'B')

    if _id==0x01:
        # pause
        pass
    elif _id==0x02:
        # resume
        pass
    elif _id==0x03:
        # set speed
        new_speed, = extract(fp, 'b')
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
        # unit/building ability
        data = extract(fp, '<H5L')
    elif _id==0x12:
        # unit/building ability
        data = extract(fp, '<H7L')
    elif _id==0x13:
        # give item to unit / drop item on ground
        data = extract(fp, '<H9L')
    elif _id==0x14:
        # unit/building ability
        data = extract(fp, '<H5L9x3L')
    elif _id==0x16:
        # change selection
        select_mode, n_units = extract(fp, '<BH')
        read(fp, 8*n_units)
    elif _id==0x17:
        # assign group hotkey
        group, n_units = extract(fp, '<BH')
        read(fp, 8*n_units)
    elif _id==0x18:
        # select group hotkey
        group, unknown = extract(fp, 'BB')
    elif _id==0x19:
        # select subgroup
        item_id, object_id1, object_id2 = extract(fp, 'LLL')
    elif _id==0x1A:
        # update subgroup
        pass
    elif _id==0x1B:
        # unknown
        extract(fp, '<BLL')
    elif _id==0x1C:
        # select ground item
        unknown, object_id1, object_id2 = extract(fp, '<BLL')
    elif _id==0x1D:
        # cancel hero revival
        read(fp, 8)
    elif _id in (0x1E, 0x1D):
        # remove unit from building qeue
        slot, item = extract(fp, '<BL')
    elif _id==0x21:
        # unknown
        read(fp, 8)
    elif _id==0x20 or 0x22<=_id<=0x32:
        # cheats
        cheat_sizes = [
                1, 0, 1, 1, 1, 1, 1,
                6, 6, 1, 1, 1, 1,
                6, 5, 1, 1, 1, 1 ]
        size = cheat_sizes[_id-0x20]
        read(fp, size)
    elif _id==0x50:
        # change ally options
        slot, flags = extract(fp, '<BL')
        print "change ally options"
        print "slot=%s flags=%s" % (slot, flags)
    elif _id==0x51:
        # transfer resources
        slot, gold, lumber = extract(fp, '<BLL')
    elif _id==0x60:
        # map trigger chat command
        unknown1, unknown2 = extract(fp, 'LL')
        message = extract_string(fp)
        #print 'trigger chat command=%s' % message
    elif _id==0x61:
        # escape pressed
        pass
    elif _id==0x62:
        # scenario trigger
        unknown1, unknown2, counter = extract(fp, 'LLL')
    elif _id==0x66:
        # enter choose hero skill submenu
        pass
    elif _id==0x67:
        # enter choose building submenu
        pass
    elif _id==0x68:
        # minimap signal
        x, y, unknown = extract(fp, 'ffL')
        # XXX: check this
    elif _id==0x69:
        # continue game (BlockB)
        read(fp, 16)
    elif _id==0x6A:
        # continue game (BlockA)
        read(fp, 16)
    elif _id==0x75:
        # unknown
        unknown, = extract(fp, 'B')
    elif _id==0x6B:
        # DotA trigger
        # see reshine.php:1162
        string_a = extract_string(fp)
        string_b = extract_string(fp)
        string_c = extract_string(fp)
        value, = extract(fp, 'L')
        #print("%-12s %-10s %-12s %-12s" % (string_a, string_b, string_c, value))
        #pprint(locals())
    else:
        raise UnknownActionException()

def parse_timeslot(game, fp):
    #print 'parse_timeslot()'
    #dumpline(read(fp, 16, False))
    n_bytes, time_increment = extract(fp, 'HH')
    fpcmd = StringIO(read(fp, n_bytes-2))

    if not eof(fpcmd):
        player_id, block_length = extract(fpcmd, '<bh')
        fpaction = StringIO(read(fpcmd, block_length))
        while not eof(fpaction):
            startpos = fpaction.tell()
            try:
                parse_action(game, fpaction)
            except Exception, ex:
                fpaction.seek(startpos)
                dumpline(read(fpaction, 24, False))
                fpaction.read()
                raise

def parse_chatmessage(game, fp):
    data = extract(fp, "<bhbl")
    sender, n_bytes, flags, mode = data
    msg = extract_string(fp)

def parse_block(game, fp):
    data = read(fp, 8, False)
    _id, = extract(fp, 'B')
    if _id in (0x1A, 0x1B, 0x1C): # start blocks
        read(fp, 4)
    elif _id==0x17:
        parse_leave(game, fp)
    elif _id in (0x1E, 0x1F): # timeslot fp
        parse_timeslot(game, fp)
    elif _id==0x20: # chat message
        parse_chatmessage(game, fp)
    elif _id==0x22: # unknown
        read(fp, 5)
    elif _id==0x23: # unknown
        read(fp, 10)
    elif _id==0x2F: # forced end game countdown
        read(fp, 8)
    elif _id==0x00: # done
        print ' --- finished --- '
        left = len(fp.read())
        print "%d bytes left" % left
    else: # failure
        print "Unknown blockid %02X" % _id
        dump(data, 'h')
        rest = fp.read()
        print "%d bytes left" % len(rest)
        raise UnknownBlockException()

    #dump(read(fp, 256, False))

def get_game(fp):
    game = {}
    game['header']  = get_header(fp)
    fpgame = unzip_gamedata(game['header'], fp)
    read(fpgame, 4)
    game['host'] = get_player(fpgame)
    game['info'] = get_gameinfo(fpgame)
    game['startrecord'] = get_gamestartrecord(fpgame)
    #pprint(gsr)

    while not eof(fpgame):
        parse_block(game, fpgame)


def usage(name):
    print "Usage: %s REPLAY-FILE" % name

if __name__=="__main__":
    import sys
    if len(sys.argv)>1:
        f = sys.argv[1]
        get_game(file(f))
    else:
        usage(sys.argv[0])

