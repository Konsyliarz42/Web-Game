from datetime import timedelta
from os.path import join, isfile
import json
import inspect

get_minutes = lambda m: (0, m) if m < 60 else (int(m/60), m - 60*int(m/60))
get_hours = lambda h: (0, h) if h < 24 else (int(h/24), h - 24*int(h/24))

def float_to_time(float_time: float):
    """This function change number to tuple with four values (days, hours, minutes, seconds).\n
    Examples:
    - float_to_time(0.01) -> (0, 0, 0, 1)
    - float_to_time(1) -> (0, 0, 1, 0)
    - float_to_time(60) -> (0, 1, 0, 0)
    - float_to_time(1440) -> (1, 0, 0, 0)"""

    float_time = float(float_time)
    days = 0
    hours = 0
    minutes = 0
    seconds = 0

    minutes, seconds = get_minutes(int(str(round(float_time%1, 2))[2:]))
    hours, x = get_minutes(int(float_time))
    minutes += x
    days, hours = get_hours(hours)
    
    return (days, hours, minutes, seconds)


def building_corrects(main_data, file_name):
    """The function is used by functions' buildings to:
    - get data from JSON file
    - set build time
    - remove non sens conditions"""

    level = main_data['level']

    # Add or change values form JSON
    if isfile(file_name):
        with open(file_name) as json_file:
            json_data = json.load(json_file)
                
            if str(level) in json_data.keys():
                main_data.update(json_data[str(level)])

    # Set build time
    # Absolute values' sum in production multiply by level
    x = [abs(v) for v in main_data['production'].values()]
    x = float_to_time(sum(x)*level)
    main_data['build_time'] = timedelta(days=x[0], hours=x[1], minutes=x[2], seconds=x[3])
    main_data['build_time_dict'] = {'days': x[0], 'hours': x[1], 'minutes': x[2], 'seconds': x[3]}

    # Remove building with negative level or zero level from buildings' conditions
    for building in [building for building in main_data['build_conditions'] if main_data['build_conditions'][building] <= 0]:
        del main_data['build_conditions'][building]

    return main_data


# =========================================================================================
# Under the comment there are functions with algorithms for generate building's dictionary.
# =========================================================================================

# M A I N   B U I L D I N G S

def house(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Dom",
        'description': "...",
        'image': "house.png",
        # Production per hour
        'production': {
            'food': -0.5*level - level
        },
        # Build
        'build_cost': {
            'wood': 100*level,
            'stone': 50*level
        },
        'build_conditions': {
            'sawmill': level - 1,
            'quarry': level - 2
        }
    }
    
    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def sawmill(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Tartak",
        'description': "...",
        'image': "sawmill.png",
        # Production per hour
        'production': {
            'food': -0.7*level - level,
            'wood': 3.0*level - level
        },
        # Build
        'build_cost': {
            'wood': 100*level,
            'stone': 100*level
        },
        'build_conditions': {
            'house': level
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def quarry(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Kamieniołom",
        'description': "...",
        'image': "quarry.png",
        # Production per hour
        'production': {
            'food': -0.7*level - level,
            'stone': 2.2*level - level
        },
        # Build
        'build_cost': {
            'wood': 100*level,
            'stone': 100*level
        },
        'build_conditions': {
            'house': level
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def barracks(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Koszary",
        'description': "...",
        'image': "barracks.png",
        # Production per hour
        'production': {
            'food': -1.0*level - level,
        },
        # Build
        'build_cost': {
            'wood': 200*level,
            'stone': 200*level
        },
        'build_conditions': {
            'house': level,
            'farm': level - 3
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def magazine(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Magazyn",
        'description': "...",
        'image': "magazine.png",
        # Production per hour
        'production': {
            'food': 0.2*level - level,
        },
        # Build
        'build_cost': {
            'wood': 200*level,
            'stone': 200*level
        },
        'build_conditions': {
            'house': level
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)

# F O O D S   P R O D U C T I O N

def farm(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Farma",
        'description': "...",
        'image': "farm.png",
        # Production per hour
        'production': {
            'food': 4.1*level,
        },
        # Build
        'build_cost': {
            'wood': 200*level,
            'stone': 200*level
        },
        'build_conditions': {
            'house': level + 1,
            'magazine': level - 5
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def windmill(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Młyn",
        'description': "...",
        'image': "windmill.png",
        # Production per hour
        'production': {
            'food': 1.4*level,
        },
        # Build
        'build_cost': {
            'wood': 400*level,
            'stone': 200*level
        },
        'build_conditions': {
            'farm': level + 5,
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def bakery(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Piekarnia",
        'description': "...",
        'image': "bakery.png",
        # Production per hour
        'production': {
            'food': 3.2*level,
        },
        # Build
        'build_cost': {
            'wood': 200*level,
            'stone': 300*level
        },
        'build_conditions': {
            'windmill': level + 2,
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)


def fishs_hut(level: int):
    main_data = {
        # Main
        'level': level,
        'name': "Rybak",
        'description': "...",
        'image': "fishs_hut.png",
        # Production per hour
        'production': {
            'food': 1.2*level,
        },
        # Build
        'build_cost': {
            'wood': 100*level,
            'stone': 40*level
        },
        'build_conditions': {
            'house': level,
        }
    }

    file_name = join(inspect.stack()[0][1], '..', inspect.stack()[0][3] + '_data.json')
    return building_corrects(main_data, file_name)

# A D V A N C E D   B U I L D I N G S
# O T H E R   B U I L D I N G S