from datetime import date
from flask_login import current_user

from .models import User, Colony
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


def get_colonies():
    """The function returns dictionaries' list with information about user's colonies."""

    if not current_user.is_authenticated:
        return None

    colonies = list()

    for colony in Colony.query.filter_by(owner=current_user.id).all():
        colonies.append({
            'id': colony.id,
            'owner': current_user.nick,
            'name': colony.name,
            'created': colony.created,
            'created_days': (date.today() - colony.created).days,
            'position': {
                'x': colony.position_x,
                'y': colony.position_y
            }
        })

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


def get_next_buildings(colony_buildings):
    """The functions returns buildings which user can build."""

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

    return buildings