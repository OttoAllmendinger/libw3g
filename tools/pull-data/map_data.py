import json
import glob
from ConfigParser import ConfigParser
import traceback
from collections import defaultdict

def get_ini_data(path):
    cp = ConfigParser()
    cp.read(path)
    return cp

def add_unit_data(unit_db, ini_data):
    for section in ini_data.sections():
        for name, value in ini_data.items(section):
            unit_db[section][name] = value

def extract_mpq(directory):
    unit_db = defaultdict(dict)
    for f in glob.glob(directory+"/*"):
        ini_data = None

        try:
            ini_data = get_ini_data(f)
        except:
            #traceback.print_exc()
            pass

        if ini_data:
            print 'data from %s' % f
            add_unit_data(unit_db, ini_data)
    return dict(unit_db)

if __name__=="__main__":
    import sys
    unit_db = extract_mpq(sys.argv[1])
    dump(unit_db)
