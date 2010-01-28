from pprint import pprint


# needed data:
#   - unit_id: unit_id
#   - name: Proper English Name,
#   - image: some image
#
# Nice to have:
#   - type: hero, unit, item, spell etc
#
# For heroes:
#   - type (strength, agility, intelligence)
#   - spells
#
# For Items:
#   - cost
#   - description

def make_data():
    map_data = get_map_data()
    www_data = get_www_data()

    for unit_id, data in sorted(map_data.items()):
        name = data.get("name")
        print unit_id, name

def find_data():
    import json
    map_data = get_map_data()
    json_data = json.load(file('units-6.60.json'))
    for k, v in sorted(json_data.items(), key=lambda (k, v): v.get('type')):
        print k, v.get('type'), \
                map_data.get(k, {}).get('__files'), \
                ('(no info at all)' if k not in map_data else '')

if __name__=="__main__":
    #make_data()
    find_data()
