import csv
import argparse
from util import *
from collections import OrderedDict


def read_dungeons():
    with open("3/LFGDungeons.csv") as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            difficulty = int(row["DifficultyID"])
            # skip open world (0) and vanilla dungeons (1) which have no lockout
            if difficulty == 0:
                continue
            key = int(row["MapID"])
            if key not in infos:
                infos[key] = {"sizes": set(), "resets": {}, "encounters": OrderedDict(), "activities": {}}
            infos[key]["expansion"] = int(row["ExpansionLevel"])
        infos[249]["legacy"] = {"expansion": 0, "size": 40}


def read_dungeon_encounter(version, ids=None):
    with open(f'{version}/DungeonEncounter.csv') as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            # Ignore Violet Hold bosses as they are random for the first 2 encounters.
            # Flags is probably a bit vector and this may be different in later expansions.
            flags = int(row["Flags"])
            if flags == 20:
                continue

            key = int(row["MapID"])
            if key not in infos or (ids is not None and key not in ids):
                continue
            order = int(row["OrderIndex"])
            name = row["Name_lang"]
            infos[key]["encounters"][order] = name
            difficulty = int(row["DifficultyID"])
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
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            reset = int(row["ResetInterval"])
            # skip instances with no lockout
            if reset == 0:
                continue
            key = int(row["MapID"])
            if key not in infos:
                print("Missing Id: " + to_string(key))
                continue
            max_players = int(row["MaxPlayers"])
            infos[key]["resets"][max_players] = reset_intervals[reset]
            infos[key]["sizes"].add(max_players)


def read_group_finder_activity():
    activity_id_lookups = {
        0: {5: [285], 10: [290], 20: [290], 40: [290]},
        1: {5: [286, 288], 10: [291], 25: [291]},
        2: {5: [287, 289, 311, 312, 314], 10: [292, 320], 25: [293, 321]},
    }
    ignore_lfg_category = {116, 118, 120}
    ignore_names = {"Trial of the Grand Crusader"}
    with open("3/GroupFinderActivity.csv") as file:
        instance_last_seen = {}
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            category = int(row["GroupFinderCategoryID"])
            name = row["ShortName_lang"]
            group = int(row["GroupFinderActivityGrpID"])
            # Ignore outdoor zones, pvp, and customer
            if category in ignore_lfg_category or name in ignore_names:
                continue
            if group == 294:
                # Ignoring holiday dungeons for now.
                continue
            key = int(row["MapID"])
            if key not in infos:
                print("Missing Id: " + to_string(key))
                continue
            # difficulty = int(row["Field_3_4_0_43659_004"])
            max_players = int(row["MaxPlayers"])
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
            activities[max_players].append(int(row["ID"]))


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-fd", "--force_download", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()
args.version = 1
update_files(args, table_names=["DungeonEncounter"])
args.version = 3
update_files(args, table_names=["DungeonEncounter", "GroupFinderActivity", "LFGDungeons", "MapDifficulty"])
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