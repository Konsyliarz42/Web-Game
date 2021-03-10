from datetime import date, datetime, timedelta
from flask_login import current_user

from .models import db, User, Colony
from .buildings.buildings import get_building

DATETIME_FORMAT = u"%Y-%m-%d %X.%f"

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
            'rapports': dict(),
            'pages': {
                'game': {'href': "/game", 'active': False, 'text': "Powrót do listy kolonii"},
                'main': {'href': f"/game/colonies/{colony.id}", 'active': False, 'text': "Główne"},
                'build': {'href': f"/game/colonies/{colony.id}/build", 'active': False, 'text': "Budowanie"},
                'production': {'href': f"/game/colonies/{colony.id}/production", 'active': False, 'text': "Produkcja"},
                'map': {'href': f"/game/colonies/{colony.id}/map", 'active': False, 'text': "Mapa"},
                'rapports': {'href': f"/game/colonies/{colony.id}/rapports", 'active': False, 'text': "Raporty"}
            }
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
    """Translate words in dictionares."""

    result = dict()
    eng = [
        'cat_main', 'cat_food', 'cat_advanced', 'cat_other', # Categories
        'wood', 'stone', 'food', 'gold', 'iron', # Resources
        'house', 'sawmill', 'quarry', 'barracks', 'magazine', 'farm', 'windmill', 'bakery', 'fish_hut', 'mine', 'ironworks', 'forge', 'mint', # Buildings
        'days', 'hours', 'minutes', 'seconds', # Time
    ]
    pol = [
        'Główne', 'Żywność', 'Zaawansowane', 'Pozostałe', # Kategorie
        'drewno', 'kamień', 'jedzenie', 'złoto', 'żelazo', # Zasoby
        'dom', 'tartak', 'kamieniołom', 'koszary', 'magazyn', 'farma', 'młyn', 'piekarnia', 'rybak', 'kopalnia', 'huta', 'kuźnia', 'mennica',  # Budynki
        'dni', 'godziny', 'minuty', 'sekundy', # Czas
    ]

    for key in dictionary:
        final_key = key
        is_list = False

        if type(dictionary[key]) == dict:
                dictionary[key] = translate_keys(dictionary[key])
        elif type(dictionary[key]) == list:
            if type(dictionary[key][1]) == dict:
                is_list = True
                pol_dict = dict()

                for k in dictionary[key][1]:
                    eng_k = k

                    if k in eng:
                        k = pol[eng.index(k)]

                    pol_dict[k] = dictionary[key][1][eng_k]
                
                pol_list = [dictionary[key][0], pol_dict]


        if key in eng:
            final_key = pol[eng.index(key)]
        
        if is_list:
            result[final_key] = pol_list
        else:
            result[final_key] = dictionary[key]

    return result


def get_next_buildings(colony_buildings, colony_resources, colony_build_now):
    """The functions returns buildings which user can build or upgrade."""

    keys = ['house', 'sawmill', 'quarry', 'barracks', 'magazine',
        'farm', 'windmill', 'bakery', 'fish_hut',
        'mine', 'ironworks', 'forge', 'mint'
    ]
    buildings = dict()

    for key in keys:
        if key not in colony_buildings.keys():
            colony_buildings[key] = {'level': 0}

        buildings[key] = get_building(name=key, level=colony_buildings[key]['level'] + 1)

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
    """The function returns main messages and:
    - Finish build
    - Update information about production
    - Add resources after every 10 minutes
    - Add rapports of production after minimum one hour from last update"""

    colony = Colony.query.filter_by(id=colony_id).first()
    messages = {
        'production': dict(),
        'production_main': dict(),
        'build': dict(),
        'hunger': colony.resources['food'][0] < 0
    }

    # End of build
    keys = list()

    for build in colony.build_now:
        building = colony.build_now[build]

        if datetime.strptime(building['build_end'], DATETIME_FORMAT) <= datetime.now():
            keys.append(build)

            # Remove trash
            for key in ['build', 'build_cost', 'build_conditions', 'build_time', 'build_time_dict', 'build_start']:
                building.pop(key)

            colony.buildings[build] = building
            messages['build'][build] = building['level']

    for key in keys:
        colony.build_now.pop(key)

    # Add build rapport
    if messages['build']:
        data = {datetime.now().__str__(): ('success', messages['build'])}

        for dt in colony.rapports:
            data[dt] = colony.rapports[dt]

        colony.rapports = data

        # Update production
        production = dict()

        for building in colony.buildings:
            for resource in colony.buildings[building]['production']:
                if resource not in production:
                    production[resource] = list()

                production[resource].append(colony.buildings[building]['production'][resource])

        for resource in production:
            if resource not in colony.resources:
                colony.resources[resource] = [0, sum(production[resource])]
            else:
                colony.resources[resource][1] = sum(production[resource])

    # Add resources
    resources = dict()

    if int(((datetime.now() - colony.last_harvest).seconds/60)/10) > 0:
        upgraded_buildings = [b for b in colony.buildings if datetime.strptime(colony.buildings[b]['build_end'], DATETIME_FORMAT) > colony.last_harvest]

        for b in colony.buildings:
            upgraded = b in upgraded_buildings
            building = colony.buildings[b]

            # Add resources before upgraded the buildings
            if upgraded:
                building_before = get_building(b, building['level'] - 1)
                production = building_before['production']
                times = (datetime.strptime(building['build_end'], DATETIME_FORMAT) - colony.last_harvest).seconds/3600

                for resource in production:
                    if resource not in resources:
                        resources[resource] = list()

                    resources[resource].append(production[resource]*times)

                times = (datetime.now() - datetime.strptime(building['build_end'], DATETIME_FORMAT)).seconds/3600
            else:
                times = (datetime.now() - colony.last_harvest).seconds/3600

            # Check actual production
            production = building['production']

            for resource in production:
                if resource not in resources:
                    resources[resource] = list()

                resources[resource].append(production[resource]*times)

        # Add resources to database
        for resource in resources:
            value = sum(resources[resource])

            # Half production if colony is hunger
            if messages['hunger']:
                value /= 2

            colony.resources[resource][0] += value

            if resource in ['wood', 'stone', 'food', 'gold']:
                messages['production_main'][resource] = value

            # Add rapport if not update for minimum one hour
            if int((datetime.now() - colony.last_harvest).seconds/3600) > 0:
                messages['production'][resource] = value
                data = {datetime.now().__str__(): ('info', messages['production'])}

                for dt in colony.rapports:
                    data[dt] = colony.rapports[dt]

                colony.rapports = data
        
        colony.last_harvest = datetime.now()
    
    # Save changes
    Colony.query.filter_by(id=colony_id).update({
        'resources': colony.resources,
        'last_harvest': colony.last_harvest,
        'buildings': colony.buildings,
        'build_now': colony.build_now,
        'rapports': colony.rapports
    })
    db.session.commit()

    print(messages, colony.last_harvest, sep='\n')
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