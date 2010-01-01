PLAYER_DATA = json.load(join(dirname(__file__), 'players.json'))

def get_players():
    return PLAYER_DATA
