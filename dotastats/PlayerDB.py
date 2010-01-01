from os.path import join

import json

class PlayerDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.players = json.load(file(join(db_path, 'players.json')))
        self.alias_map = self._aliasmap(self.players)

    def _aliasmap(self, players):
        alias_map = {}
        for k, v in players.items():
            for alias in v['aliases']:
                alias_map[alias] = k
        return alias_map
