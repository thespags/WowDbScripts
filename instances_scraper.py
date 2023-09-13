import csv
import argparse
from util import *
from collections import OrderedDict


def read_dungeons():
    with open("3/LFGDungeons.csv") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        id_index = get_key(header, "MapID")
        difficulty_id_index = get_key(header, "DifficultyID")
        expansion_index = get_key(header, "ExpansionLevel")
        # name_index = get_key(header, "Name_lang")

        for row in csvreader:
            difficulty = int(row[difficulty_id_index])
            # skip open world (0) and vanilla dungeons (1) which have no lockout
            if difficulty == 0:
                continue
            key = int(row[id_index])
            if key not in infos:
                infos[key] = {"sizes": set(), "resets": {}, "encounters": OrderedDict(), "activities": {}}
            infos[key]["expansion"] = int(row[expansion_index])
        infos[249]["legacy"] = {"expansion": 0, "size": 40}


def read_dungeon_encounter(version, ids=None):
    with open("{0}/DungeonEncounter.csv".format(version)) as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        id_index = get_key(header, "MapID")
        difficulty_index = get_key(header, "DifficultyID")
        order_index = get_key(header, "OrderIndex")
        name_index = get_key(header, "Name_lang")
        flags_index = get_key(header, "Flags")

        for row in csvreader:
            # Ignore Violet Hold bosses as they are random for the first 2 encounters.
            # Flags is probably a bit vector and this may be different in later expansions.
            flags = int(row[flags_index])
            if flags == 20:
                continue

            key = int(row[id_index])
            if key not in infos or (ids is not None and key not in ids):
                continue
            order = int(row[order_index])
            name = row[name_index]
            infos[key]["encounters"][order] = name
            difficulty = int(row[difficulty_index])
            if key not in name_to_difficulty:
                name_to_difficulty[key] = {}
            name_to_difficulty[key][name] = difficulty


def sort_encounters():
    # sort by order index
    for k, v in infos.items():
        sorted_v = []
        for _, encounter in sorted(v["encounters"].items()):
            sorted_v.append(encounter)
        infos[k]["encounters"] = sorted_v
        index = len(sorted_v)
        difficulty = 2
        while difficulty == 2:
            index -= 1
            difficulty = name_to_difficulty[k][sorted_v[index]]
        infos[k]["lastBossIndex"] = index + 1


def read_map_difficulty():
    reset_intervals = {1: 1, 2: 7, 3: 3, 4: 5}
    with open("3/MapDifficulty.csv") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        id_index = get_key(header, "MapID")
        reset_index = get_key(header, "ResetInterval")
        max_players_index = get_key(header, "MaxPlayers")

        for row in csvreader:
            reset = int(row[reset_index])
            # skip instances with no lockout
            if reset == 0:
                continue
            key = int(row[id_index])
            if key not in infos:
                print("Missing Id: " + to_string(key))
                continue
            max_players = int(row[max_players_index])
            infos[key]["resets"][max_players] = reset_intervals[reset]
            infos[key]["sizes"].add(max_players)


def read_group_finder_activity():
    activity_id_lookups = {
        0: {5: [285], 10: [290], 20: [290], 40: [290]},
        1: {5: [286, 288], 10: [291], 25: [291]},
        2: {5: [287, 289, 311, 312, 314], 10: [292], 25: [293]},
    }
    ignore_lfg_category = {116, 118, 120}
    ignore_names = {"Trial of the Grand Crusader"}
    with open("3/GroupFinderActivity.csv") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        id_index = get_key(header, "MapID")
        value_index = get_key(header, "ID")
        name_index = get_key(header, "FullName_lang")
        # difficulty_index = get_key(header, "Field_3_4_0_43659_004")
        category_index = get_key(header, "GroupFinderCategoryID")
        group_index = get_key(header, "GroupFinderActivityGrpID")
        max_players_index = get_key(header, "MaxPlayers")
        instance_last_seen = {}

        for row in csvreader:
            category = int(row[category_index])
            name = row[name_index]
            group = int(row[group_index])
            # Ignore outdoor zones, pvp, and customer
            if category in ignore_lfg_category or name in ignore_names:
                continue
            if group == 294:
                # Ignoring holiday dungeons for now.
                continue
            key = int(row[id_index])
            if key not in infos:
                print("Missing Id: " + to_string(key))
                continue
            # difficulty = int(row[difficulty_index])
            max_players = int(row[max_players_index])
            activities = infos[key]["activities"]
            if max_players not in activities:
                activities[max_players] = []
            # Dungeons released later than old Titan Rune dungeons don't get an id.
            if key in instance_last_seen:
                expected_groups = activity_id_lookups[infos[key]["expansion"]][max_players]
                index = expected_groups.index(group)
                expected = max_players in activities and len(activities[max_players]) or 0
                while expected < index:
                    expected += 1
                    activities[max_players].append("nil")
            instance_last_seen[key] = group
            activities[max_players].append(int(row[value_index]))


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-f", "--force", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()
update_files(1, args.download, args.force, "DungeonEncounter")
update_files(3, args.download, args.force, "DungeonEncounter", "GroupFinderActivity", "LFGDungeons", "MapDifficulty")
name_to_difficulty = {}
infos = {}
read_dungeons()
# For whatever reason these instances aren't in the db for Wotlk but do exist...
read_dungeon_encounter(1, ids={34, 289})
read_dungeon_encounter(3)
sort_encounters()
read_map_difficulty()
read_group_finder_activity()

Path("instances").mkdir(parents=True, exist_ok=True)
f = open("instances/instances.lua", "w")
f.write("infos = " + to_string(infos))
f.write("""

for k, v in pairs(infos) do
    infos[k] = Instances:new(v)
    v.id = k
end""")
f.close()
print("instances.lua written...")