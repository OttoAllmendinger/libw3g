from os.path import exists, join, dirname

import json
import glob
from ConfigParser import ConfigParser
import traceback
from collections import defaultdict

from pprint import pprint

DOTA_MAP_DIR = "dota_map"

if not exists(DOTA_MAP_DIR):
    raise "please extract your dota map to the directory dota_map"

def get_ini_data(path):
    cp = ConfigParser()
    cp.read(path)
    return cp

def add_unit_data(unit_db, ini_data, path):
    file_id = int(path
            .replace(join(DOTA_MAP_DIR, 'file'), '')
            .replace('.xxx', ''))
    for section in ini_data.sections():
        for name, value in ini_data.items(section):
            unit_db[section][name] = value

        if not '__files' in unit_db[section]:
            unit_db[section]['__files'] = [file_id]
        else:
            unit_db[section]['__files'].append(file_id)

def ini_files():
    for path in glob.glob(join(DOTA_MAP_DIR, '*')):
        try:
            yield path, get_ini_data(path)
        except:
            pass

def list_ini_files():
    for path, data in ini_files():
        print path

def get_map_data():
    unit_db = defaultdict(dict)
    for path, data in ini_files():
        add_unit_data(unit_db, data, path)
    return dict(unit_db)

def map_fname(n):
    return join(DOTA_MAP_DIR, 'file%06d.xxx' % n)

def get_map_data0():
    unit_db = defaultdict(dict)
    add_unit_data(unit_db, get_ini_data(map_fname(308)), 308)
    return dict(unit_db)

def dump():
    pprint(get_map_data())


if __name__=="__main__":
    import sys
    if '--list' in sys.argv:
        list_ini_files()
    if '--dump' in sys.argv:
        dump()

