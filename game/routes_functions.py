from datetime import date, datetime
from flask_login import current_user

from .models import db, User, Colony
from .buildings.buildings import house, sawmill, quarry, magazine, barracks, farm, windmill, bakery, fish_hut, mine, forge, ironworks, mint

def get_user():
    """The functions returns dictionary with information about current user."""
    
    if current_user.is_authenticated:
        return {
            'id': current_user.id,
            'nick': current_user.nick,
            'email': current_user.email,
            'created': current_user.created,
            'created_days': (date.today() - current_user.created).days,
            'colonies': current_user.colonies
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
            'build_now': colony.build_now,
            'last_harvest': colony.last_harvest,
            'resources': colony.resources,
            'buildings': colony.buildings,
            'main_resources': {
                'wood': colony.resources['wood'],
                'stone': colony.resources['stone'],
                'food': colony.resources['food'],
                'gold': colony.resources['gold']
            },
            'rapports': dict()
        }

        for dt in colony.rapports:
            if dt[:10] == date.today().__str__():
                c['rapports'][dt] = colony.rapports[dt]
            else:
                break

        # Return colony with colony_id
        if colony_id and c['id'] == colony_id:
            return c

        colonies.append(c)

    return colonies


def translate_keys(dictionary):
    """Translate name of resources and buildings."""

    result = dict()
    items_keys = [
        'cat_main', 'cat_food', 'cat_advanced', 'cat_other', # Categories
        'wood', 'stone', 'food', 'gold', # Resources
        'house', 'sawmill', 'quarry', # Buildings
        'days', 'hours', 'minutes', 'seconds', # Time
    ]
    keys = [
        'Główne', 'Żywność', 'Zaawansowane', 'Pozostałe', # Kategorie
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


def get_next_buildings(colony_buildings, colony_resources, colony_build_now):
    """The functions returns buildings which user can build or upgrade."""

    keys = ['house', 'sawmill', 'quarry', 'barracks', 'magazine',
        'farm', 'windmill', 'bakery', 'fish_hut',
        'mine', 'ironworks', 'forge', 'mint'
    ]

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
        'fish_hut': fish_hut(colony_buildings['fish_hut']['level'] + 1),

        'mine': mine(colony_buildings['mine']['level'] + 1),
        'ironworks': ironworks(colony_buildings['ironworks']['level'] + 1),
        'forge': forge(colony_buildings['forge']['level'] + 1),
        'mint': mint(colony_buildings['mint']['level'] + 1)
    }

    for b in buildings:
        conditions = buildings[b]['build_conditions']
        buildings[b]['build_allow'] = True
        buildings[b]['build'] = False

        # Limit of build
        if len(colony_build_now) >= 3:
            buildings[b]['build_allow'] = False
        else:
            # Check build conditions
            try:
                for c in conditions.keys():
                    if colony_buildings[c]['level'] < conditions[c]:
                        buildings[b]['build_allow'] = False
                        break
            except KeyError:
                buildings[b]['build_allow'] = False

            # Check build cost
            if buildings[b]['build_allow']:
                cost = buildings[b]['build_cost']

                for c in cost.keys():
                    if colony_resources[c][0] < cost[c]:
                        buildings[b]['build_allow'] = False
                        break

            # Check is building on build list?
            if b in colony_build_now:
                buildings[b]['build_allow'] = False
                buildings[b]['build'] = True

    return buildings


def update_colony(colony_id):
    """Use this function in get method in all colonies' pages!\n
    The function update data of colony. (adding resources, ending building)"""

    colony = Colony.query.filter_by(id=colony_id).first()
    delete_key = list()
    messages = {'production': dict(), 'production_main': dict() , 'build': dict()}

    # Add resources
    times = round((datetime.now() - colony.last_harvest).seconds/3600)
    hunger = False

    if colony.resources['food'][0] < 0:
        hunger = True

    for resource in colony.resources:
        production = colony.resources[resource][1]

        if hunger:
            production /= 2

        colony.resources[resource][0] += times*production

        if times*production != 0:
            messages['production'][resource] = times*production

            if resource in ['wood', 'stone', 'food']:
                messages['production_main'][resource] = messages['production'][resource]
    
    if times:
        print(messages)
        colony.last_harvest = datetime.now()

    messages['hunger'] = hunger

    # End build
    for building in colony.build_now.keys():
        b = colony.build_now[building]

        if datetime.today() >= datetime.strptime(b['build_end'], u"%Y-%m-%d %X.%f"):
            for r in b['production']:
                if r not in colony.resources:
                    colony.resources[r] = [0, b['production'][r]]

                if building in colony.buildings:
                    res_production = b['production'][r] - colony.buildings[building]['production'][r]
                    colony.resources[r][1] += res_production

            colony.buildings[building] = b
            delete_key.append(building)
            messages['build'][building] = b['level']
        else:
            break

    for key in delete_key:
        colony.build_now.pop(key)

    # Add to rapports
    if messages['production']:
        data = {datetime.now().__str__(): ('info', translate_keys(messages['production']))}

        for dt in colony.rapports:
            data[dt] = colony.rapports[dt]

        colony.rapports = data

    if messages['build']:
        data = {datetime.now().__str__(): ('success', translate_keys(messages['build']))}

        for dt in colony.rapports:
            data[dt] = colony.rapports[dt]

        colony.rapports = data

    # Save changes
    Colony.query.filter_by(id=colony_id).update({
        'resources': colony.resources,
        'last_harvest': colony.last_harvest,
        'buildings': colony.buildings,
        'build_now': colony.build_now,
        'rapports': colony.rapports
    })
    db.session.commit()

    return messages


def get_map():

    # Create empty map
    positions = dict()
    for x in range(10):
        positions[x] = dict()

        for y in range(10):
            positions[x][y] = None

    # Add colonies to the map
    for colony in Colony.query.all():
        x = colony.position_x
        y = colony.position_y

        positions[x][y] = {
            'id': colony.id,
            'owner': current_user.nick,
            'name': colony.name,
            'created': colony.created,
            'created_days': (date.today() - colony.created).days,
            'position': {
                'x': colony.position_x,
                'y': colony.position_y
            }
        }

    return positions