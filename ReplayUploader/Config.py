import json

Config = {}

configFile = join(expanduser("~", "dru.config"))

if exists(configFile):
    Config.update(json.load(file(configFile, 'r')))

def saveConfig():
    json.dump(Config, file(configFile, 'w'))
