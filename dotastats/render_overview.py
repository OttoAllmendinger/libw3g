from os.path import *
from genshi.template import TemplateLoader
from random import randint, choice

TITLES = ['Friday', 'Saturday', 'Sunday']

PLAYERS = ('Bizarr-Mina', 'Otto', 'inside', 'wrdlbrmpf', 'Safarikondom',
        'das schrauberle')


def get_players():
    #return (dict(name=p) for p in PLAYERS)
    return PLAYERS

def some(total, fraction):
    return filter(lambda x: randint(0, 100)<(fraction*100), total)

def get_player_stats():
    return dict((player, dict(
        is_winner=choice((True, False)),
        hero_id=choice(('0001', '0002')),
        kills=randint(0, 20))) for player in some(get_players(), .75))

def get_hero_image(hero_id):
    return 'img/%s.png' % hero_id

def get_games():
    return (dict(players=get_player_stats()) for n in range(randint(10, 20)))

def get_play_days():
    return (dict(title=t, games=get_games()) for t in TITLES)


loader = TemplateLoader(join(dirname(__file__), 'html'), auto_reload=True)
data = loader.load('overview.tpl.html').generate( get_hero_image=get_hero_image,
        play_days=get_play_days(), players=get_players()).render('html')

file(expanduser('~/tmp/overview.render.html'), 'w').write(data)
