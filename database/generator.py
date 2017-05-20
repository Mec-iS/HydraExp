import random
import json
import psycopg2 as psql

subsystems = dict({
    "communication" : {
        "slug": "COM",
        "ontology": "http://ontology.projectchronos.eussubsystems/Spacecraft_Communication",
        "power": {"min": -200, "max": -1},
        "mass": {"min": 30, "max": 100},
        "cost": {"min": 1000, "max": 10000},
        "minWorkingTemp": { "min": -40, "max": -20 },
        "maxWorkingTemp": { "min": 40, "max": 90 }
    },
    "propulsion" : {
        "slug": "PROP",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Propulsion",
        "power": {"min": -200, "max": -50},
        "mass": {"min": 10, "max": 100},
        "cost": {"min": 5000, "max": 25000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "detector" : {
        "slug": "DTR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Detector",
        "power": {"min": -100, "max": -10},
        "mass": {"min": 50, "max": 400},
        "cost": {"min": 2000, "max": 15000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "primary power" : {
        "slug": "PPW",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_PrimaryPower",
        "power": {"min": 200, "max": 2000},
        "density" : 1.5,
        "mass": {"min": 30, "max": 100},
        "cost": {"min": 2000, "max": 10000},
        "minWorkingTemp": { "min": -60, "max": -40 },
        "maxWorkingTemp": { "min": 50, "max": 100 }
    },
    "backup power" : {
        "slug": "BCK",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_BackupPower",
        "power": {"min": 50, "max": 1500},
        "density": 2,
        "mass": {"min": 100, "max": 300},
        "cost": {"min": 5000, "max": 25000},
        "minWorkingTemp": { "min": -30, "max": -10 },
        "maxWorkingTemp": { "min": 20, "max": 80 }
    },
    "thermal" : {
        "slug": "THR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Thermal",
        "power": {"min": -100, "max": 100},
        "mass": {"min": 20, "max": 150},
        "cost": {"min": 500, "max": 4000},
        "minTemperature": { "min": -100, "max": -30 },
        "maxTemperature": { "min": 50, "max": 100 }
    },
    "structure" : {
        "slug": "STR",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_Structure",
        "mass": {"min": 10, "max": 100},
        "cost": {"min": 2000, "max": 35000},
        "minWorkingTemp": { "min": -90, "max": -30 },
        "maxWorkingTemp": { "min": 30, "max": 70 }
    },
    "command and data" : {
        "slug": "CDH",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_CDH",
        "power": {"min": -50, "max": -5},
        "mass": {"min": 20, "max": 70},
        "cost": {"min": 1000, "max": 5000},
        "minWorkingTemp": { "min": -20, "max": -10 },
        "maxWorkingTemp": { "min": 10, "max": 50 }
    },
    "attitude and orbit control" : {
        "slug": "AODCS",
        "ontology": "http://ontology.projectchronos.eu/subsystems/Spacecraft_AODCS",
        "power": {"min": -150, "max": 100},
        "mass": {"min": 10, "max": 80},
        "cost": {"min": 1000, "max": 15000},
        "minWorkingTemp": { "min": -50, "max": -30 },
        "maxWorkingTemp": { "min": 30, "max": 70 },
        "active": ["magnetic torque", "cold gas", "microthrusters"],
        "passive": ["rotation", "gravity", "solar pressure"]
    }
})


def random_value(interval):
    """
    Generates a random integer value from a given interval
    """
    if not isinstance(interval, dict):
        raise ValueError('value has to be dict')
    return random.randrange(interval['min'], interval['max'], 1) // 1


def generate_object(name, subsystem):
    """
    Generates random components from given input dictionary
    """
    result = {}
    result['mass'] = random_value(subsystem['mass'])
    result['category'] = name
    if 'minWorkingTemp' in subsystem.keys(): # general rule
        if not name == 'structure':
            result['power'] = random_value(subsystem['power'])
        result['minWorkingTemp'] = random_value(subsystem['minWorkingTemp'])
        result['maxWorkingTemp'] = random_value(subsystem['maxWorkingTemp'])
        if 'density' in subsystem.keys():  # rule power or battery
            result['volume'] = int(result['mass'] / subsystem['density']) // 1
            if name == 'primary power':
                result['cost'] = result['power'] * 5
                return result
            elif name == 'backup power':
                result['cost'] = result['power'] * 16
                return result
        else:    # rule for other not generator
            result['volume'] = result['mass'] + random_value({'min': -5, 'max': 5})
            if name not in ['structure', 'attitude and orbit control']:
                if name == 'detector':
                    result['type'] = random.choice(['interferometer', 'spectrometer', 'photometer', 'optical', 'dust detector'])

                result['cost'] = random_value(subsystem['cost'])
                return result
            else:
                if name == 'structure':
                    result['power'] = 0
                    result['cost'] = int(350000 / result['mass']) // 1
                    return result
                elif name == 'attitude and orbit control':
                    if result['power'] > 0:
                        result['power'] = 0
                        result['type'] = 'passive'
                        result['mechanism'] = random.choice(subsystem['passive'])
                    else:
                        result['type'] = 'active'
                        result['mechanism'] = random.choice(subsystem['active'])
                    result['cost'] = random_value(subsystem['cost'])
                    return result

    else: # rule for thermal
        result['volume'] = result['mass'] + random_value({'min': -5, 'max': 5})
        result['power'] = random_value(subsystem['power'])
        if result['power'] > 0 : result['power'] = 0
        result['minTemperature'] = random_value(subsystem['minTemperature'])
        result['maxTemperature'] = random_value(subsystem['maxTemperature'])

        result['cost'] = (result['maxTemperature'] - result['minTemperature']) * 20

        if result['power'] == 0:
            result['type'] = 'passive'
        else:
            result['type'] = 'active'
        return result

def gen_all_types():
    output = []
    global subsystems
    i = 0
    for k, v in subsystems.items():
        # print(k)
        name = str(random.randrange(0, 50)) + str(random.choice(['T', 'W', 'KV', 'JFG'])) + ' ' + k
        obj = {}
        obj['name'] = name
        obj['id'] = i + 1
        obj['object'] = generate_object(k, v)
        output.append(obj)
        i+=1
    return output

def insert_data(entries):
    db_credentials = "dbname='hydra' user='hydrus' host='localhost' password='hydra'"
    conn = psql.connect(db_credentials)
    cur = conn.cursor()
    for i in range(entries):
        objects = gen_all_types()
        for subsystem in objects:
            name = subsystem["name"]
            obj = subsystem["object"]
            relation = subsystems[obj["category"]]["slug"]
            cur.execute('INSERT INTO SubSystem (name, category) VALUES(%s, %s) RETURNING ID', (name, relation))
            sub_id = cur.fetchone()[0]
            command =""
            if relation in ['COM', "PROP", "PPW", "BCK", "STR", "CDH"]:
                command = "INSERT INTO {} VALUES ({}, {}, {}, {}, {}, {}, {})".format(
                relation, sub_id, obj["power"], obj["mass"],
                obj["cost"], obj["volume"], obj["minWorkingTemp"], obj["maxWorkingTemp"]
                )
            elif relation == "THR":
                command = "INSERT INTO {} VALUES ({}, {}, {}, {}, {}, '{}', {}, {})".format(
                relation, sub_id, obj["power"], obj["mass"], obj["cost"],
                obj["volume"], str(obj["type"]), obj["minTemperature"], obj["maxTemperature"]
                )
            elif relation == "DTR":
                command = "INSERT INTO {} VALUES ({}, {}, {}, {}, {}, '{}', {}, {})".format(
                relation, sub_id, obj["power"], obj["mass"], obj["cost"],
                obj["volume"], str(obj["type"]), obj["minWorkingTemp"], obj["maxWorkingTemp"]
                )
            elif relation == "AODCS":
                command = "INSERT INTO {} VALUES ({}, {}, {}, {}, {}, '{}', '{}', {}, {})".format(
                relation, sub_id, obj["power"], obj["mass"], obj["cost"], obj["volume"],
                obj["type"], str(obj["mechanism"]), obj["minWorkingTemp"], obj["maxWorkingTemp"]
                )
            cur.execute(command)
            conn.commit()
    cur.close()
    conn.close()
    return None


if __name__=="__main__":
    # print(json.dumps(gen_all_types(), indent=4))
    insert_data(2)
