import json

_data = json.load(file('units-6.60.json'))

def id_to_name():
    for k, v in sorted(_data.items()):
        print k, v['name']


if __name__=="__main__":
    id_to_name()
