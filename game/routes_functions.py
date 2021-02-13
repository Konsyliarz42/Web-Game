from datetime import date, datetime
from flask_login import current_user

from .models import db, User, Colony
from .buildings.buildings import house, sawmill, quarry, magazine, barracks, farm, windmill, bakery, fishs_hut

def get_user():
    """The functions returns dictionary with information about current user."""
    
    if current_user.is_authenticated:
        return {
            'id': current_user.id,
            'nick': current_user.nick,
            'email': current_user.email,
            'created': current_user.created,
            'created_days': (date.today() - current_user.created).days
        }


def get_colonies(colony_id=None):
    """The function returns dictionaries' list with information about user's colonies."""

    if not current_user.is_authenticated:
        return None

    colonies = list()

    for colony in Colony.query.filter_by(owner=current_user.id).all():
        c = {
            'id': colony.id,
            'owner': current_user.nick,
            'name': colony.name,
            'created': colony.created,
            'created_days': (date.today() - colony.created).days,
            'position': {
                'x': colony.position_x,
                'y': colony.position_y
            },
            'build_now': colony.build_now
        }

        # Return colony with colony_id
        if colony_id and c['id'] == colony_id:
            return c

        colonies.append(c)

    return colonies


def translate_keys(dictionary):
    """Translate name of resources and buildings."""

    result = dict()
    items_keys = [
        'wood', 'stone', 'food', 'gold', # Resources
        'house', 'sawmill', 'quarry', # Buildings
        'days', 'hours', 'minutes', 'seconds', # Time
    ]
    keys = [
        'drewno', 'kamień', 'jedzenie', 'złoto', # Zasoby
        'dom', 'tartak', 'kamieniołom', # Budynki
        'dni', 'godziny', 'minuty', 'sekundy', # Czas
    ]

    for key in dictionary:
        final_key = key

        if type(dictionary[key]) == dict:
                dictionary[key] = translate_keys(dictionary[key])

        if key in items_keys:
            final_key = keys[items_keys.index(key)]
        
        result[final_key] = dictionary[key]

    return result


def get_next_buildings(colony_buildings, colony_resources):
    """The functions returns buildings which user can build or upgrade."""

    keys = ['house', 'sawmill', 'quarry', 'barracks', 'magazine', 'farm', 'windmill', 'bakery', 'fishs_hut']

    for key in keys:
        if key not in colony_buildings.keys():
            colony_buildings[key] = {'level': 0}

    buildings = {
        'house': house(colony_buildings['house']['level'] + 1),
        'sawmill': sawmill(colony_buildings['sawmill']['level'] + 1),
        'quarry': quarry(colony_buildings['quarry']['level'] + 1),
        'barracks': barracks(colony_buildings['barracks']['level'] + 1),
        'magazine': magazine(colony_buildings['magazine']['level'] + 1),
        
        'farm': farm(colony_buildings['farm']['level'] + 1),
        'windmill': windmill(colony_buildings['windmill']['level'] + 1),
        'bakery': bakery(colony_buildings['bakery']['level'] + 1),
        'fishs_hut': fishs_hut(colony_buildings['fishs_hut']['level'] + 1)
    }

    for b in buildings:
        conditions = buildings[b]['build_conditions']
        buildings[b]['build_allow'] = True

        # Check build conditions
        for c in conditions.keys():
            if colony_buildings[c]['level'] < conditions[c]:
                buildings[b]['build_allow'] = False
                break

        # Check build cost
        if not buildings[b]['build_allow']:
            cost = buildings[b]['build_cost']

            for c in cost.keys():
                if colony_resources[c][0] < cost[c]:
                    buildings[b]['build_allow'] = False
                    break

    return buildings


def update_colony(colony_id):

    colony = Colony.query.filter_by(id=colony_id).first()
    delete_key = list()

    # End build
    for building in colony.build_now.keys():
        b = colony.build_now[building]

        print(b['build_end'])
        if datetime.today() >= datetime.strptime(b['build_end'], u"%Y-%m-%d %X.%f"):
            colony.buildings[building] = b
            delete_key.append(building)
        else:
            break

    for key in delete_key:
        colony.build_now.pop(key)

    # Save changes
    Colony.query.filter_by(id=colony_id).update({
        'resources': colony.resources,
        'buildings': colony.buildings,
        'build_now': colony.build_now
    })
    db.session.commit()