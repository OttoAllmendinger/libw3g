from os.path import join, expanduser
import json

config_file = join(expanduser("~"), "dru.config.json")

def load():
    try:
        return json.load(file(config_file, 'r'))
    except:
        return {}

def save(cfg):
    json.dump(cfg, file(config_file, 'w'))

def get(key, default=None):
    return load().get(key, default)

def set(key, value):
    cfg = load()
    cfg[key]=value
    save(cfg)
