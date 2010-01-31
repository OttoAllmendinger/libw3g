import glob
import json
import urllib2
import re

from collections import defaultdict
from os.path import exists, join, expanduser
from pprint import pprint

from BeautifulSoup import BeautifulSoup
from configobj import ConfigObj

DIR_DOTAMAP = "dota_map"
URL_WEBDATA_HERO = "http://www.playdota.com/cache/hero.js"
URL_WEBDATA_ITEM = "http://www.playdota.com/cache/items.js"
FN_CACHE_INIDATA = 'inidata.json'
FN_CACHE_WEBDATA_HERO = "webdata_hero.json"
FN_CACHE_WEBDATA_ITEM = "webdata_items.json"
UNIT_HERO = "hero"
UNIT_ITEM = "item"

if not exists(DIR_DOTAMAP):
    raise "please extract your dota map to the directory dota_map"

def cache_hash(tag):
    return hashlib.md5(tag).hexdigest()

def from_cache(tag):
    return join(CACHEDIR, cache_hash())

def inidata_files():
    for path in glob.glob(join(DIR_DOTAMAP, '*')):
        try:
            yield path, dict(ConfigObj(path))
        except:
            pass

def get_inidata():
    if exists(FN_CACHE_INIDATA):
        return json.load(file(FN_CACHE_INIDATA))

    unit_db = defaultdict(dict)
    for path, data in inidata_files():
        for k, v in data.items():
            if len(k)==4:
                unit_db[k].update(v)

    json.dump(unit_db, file(FN_CACHE_INIDATA, 'w'))

    return dict(unit_db)

def webdata_getsource(url, cachefile):
    if exists(cachefile):
        data = file(cachefile).read()
    else:
        data = urllib2.urlopen(url).read()
        file(cachefile, 'w').write(data)
    return data

def webdata_unescape(text):
    def hex2int(match):
        return unichr(int(match.group(0)[1:], 16))
    return re.sub(r"%..", hex2int, text)

def webdata_parsejs(unit_type, data):
    if unit_type==UNIT_HERO:
        HD = {}
        for n, line in enumerate(data.splitlines()):
            if re.search(r"^HD\[\d*\]", line):
                exec line # ridicoulusly unsafe
        return HD

    elif unit_type==UNIT_ITEM:
        IT = {}
        for n, line in enumerate(data.splitlines()):
            if re.search(r"^IT\[\d*\]", line):
                exec line # ridicoulusly unsafe
        return IT

def webdata_parsehtml(soup):
    key = int(soup.hero.key.string)
    hclass = int(soup.hero.hclass.string)
    class_ = soup.hero.find('class').string.strip()
    name = soup.hero.find('name').string.strip()
    file(expanduser("~/tmp/hero%d.html" % key), 'w').write(soup.prettify())
    return key, dict(key=key, hclass=hclass, name=name,
            class_=class_)

def get_webdata():
    _UNIT_TYPES = [
            (UNIT_HERO, URL_WEBDATA_HERO, FN_CACHE_WEBDATA_HERO),
            (UNIT_ITEM, URL_WEBDATA_ITEM, FN_CACHE_WEBDATA_ITEM) ]

    for unit_type, unit_db_url, cachefile in _UNIT_TYPES:
        unit_defs = webdata_parsejs(
                unit_type, webdata_getsource(unit_db_url, cachefile))
        unit_db = {}

        for k, v in unit_defs.items():
            soup = BeautifulSoup(webdata_unescape(v))
            unit_id, unit_data = webdata_parsehtml(soup)
            unit_db[unit_id] = unit_data
            unit_db[unit_id]['__type'] = unit_type

    return unit_db

def make_data():
    webdata = get_webdata()
    inidata = get_inidata()

    webdata_byname = dict((v['class_'], v) for v in webdata.values())

    merged_data = {}
    assigned_ids = defaultdict(list)

    #pprint(webdata)
    _NAMEKEY = 'Name'

    for k, v in inidata.items():
        if _NAMEKEY in v:
            name = v[_NAMEKEY]
            if isinstance(v[_NAMEKEY], list):
                name = name[0]
            if name in webdata_byname:
                print 'Found %s in webdata' % name
                merged_data[k] = webdata_byname[name]['key']
                assigned_ids[name].append(k)
            else:
                pass
                #print 'Didn\'t find %s in webdata' % name

    print 'merged_data: %d' % len(merged_data)
    print 'webdata: %d' % len(webdata)
    print 'webdata_byname: %d' % len(webdata_byname)
    print 'assigned_ids: %d' % len(assigned_ids)
    pprint(dict(assigned_ids))
    pprint(dict(merged_data))

if __name__=="__main__":
    #dump_ini(unitdb_from_ini())
    #pprint(unitdb_from_ini())
    make_data()
