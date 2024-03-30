import csv
from util import *
from collections import OrderedDict


def read_dungeons(version):
    with read_table(version, "LFGDungeons") as file:
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
            group_id = int(row["Group_ID"])
            activity_id = int(row["ID"])
            infos[key]["activities"][group_id] = activity_id
        infos[249]["legacy"] = {"expansion": 0, "size": 40}


def read_dungeon_encounter(version, ids=None):
    with read_table(version, "DungeonEncounter") as file:
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


def read_map_difficulty(version):
    reset_intervals = {1: 1, 2: 7, 3: 3, 4: 5}
    with read_table(version, "MapDifficulty") as file:
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


def read_dungeon_groups(version):
    with read_table(version, "LFGDungeonGroup") as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            groups[int(row["ID"])] = row["Name_lang"]


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-fd", "--force-download", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()
args.version = 1
update_files(args, table_names=["DungeonEncounter"])
args.version = 3
update_files(args, table_names=["DungeonEncounter", "LFGDungeons", "LFGDungeonGroup", "MapDifficulty"])
name_to_difficulty = {}
infos = {}
groups = {}
read_dungeons(args.version)
# For whatever reason these instances aren't in the db for Wotlk but do exist...
read_dungeon_encounter(1, ids={34, 289})
read_dungeon_encounter(args.version)
sort_encounters()
read_map_difficulty(args.version)
read_dungeon_groups(args.version)

Path("instances").mkdir(parents=True, exist_ok=True)
with open("instances/instances.lua", "w") as f:
    f.write("groups = " + to_string(groups))
    f.write("\n\ninfos = " + to_string(infos))
    f.write("""
    
    for k, v in pairs(infos) do
        infos[k] = Instances:new(v)
        v.id = k
    end""")
print("instances.lua written...")