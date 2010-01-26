import map_data
import web_data

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

    map_data = map_data.get_map_data()
    web_data = web_data.get_web_data()

    for unit_id, data in map_data.items():
        name = unit.get("name")

