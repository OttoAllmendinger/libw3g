from BeautifulSoup import BeautifulSoup

import urllib2
import re

HERO_DATA_URL = "http://www.playdota.com/cache/hero.js"

def get_data_www():
    return urllib2.urlopen(HERO_DATA_URL).read()

def get_data_fs():
    return file("hero.js").read()

def unescape(text):
    def hex2int(match):
        return unichr(int(match.group(0)[1:], 16))
    return re.sub(r"%..", hex2int, text)

def get_hero_definitions(data):
    HD = {}
    for n, line in enumerate(data.splitlines()):
        if re.search(r"^HD\[\d*\]", line):
            exec line # ridicoulusly unsafe
    return HD

def get_hero_info(soup):
    key = int(soup.hero.key.string)
    hclass = int(soup.hero.hclass.string)
    name = soup.hero.name.strip()
    return key, dict(key=key, hclass=hclass, name=name)

def get_hero_db(data):
    hero_defs = get_hero_definitions(data)
    hero_db = {}

    for k, v in hero_defs.items():
        soup = BeautifulSoup(unescape(v))
        hero_id, hero_info = get_hero_info(soup)
        hero_db[hero_id] = hero_info

    return hero_db

def convert(data):
    hero_db_www = get_hero_db(data)


if __name__=="__main__":
    #convert(get_data_www())
    convert(get_data_fs())
    pass
