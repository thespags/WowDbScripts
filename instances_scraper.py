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
            # Skip pre patch zone.
            if key == 734:
                continue
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


args = parse_args()
# args.version = 1
# update_files(args, table_names=["DungeonEncounter"])
update_files(args, table_names=["DungeonEncounter", "LFGDungeons", "LFGDungeonGroup", "MapDifficulty"])
name_to_difficulty = {}
infos = {}
read_dungeons(args.version)
# For whatever reason these instances aren't in the db for Wotlk but do exist...
read_dungeon_encounter(1, ids={34, 289})
read_dungeon_encounter(args.version)
sort_encounters()
read_map_difficulty(args.version)

Path(f"instances/{args.version}").mkdir(parents=True, exist_ok=True)
with open(f"instances/{args.version}/instances.lua", "w") as f:
    f.write(f"""local lib = LibStub("LibInstances")

if {args.version} < LE_EXPANSION_LEVEL_CURRENT 
    {f"and {args.version} > LE_EXPANSION_LEVEL_CURRENT" if args.version == 4 else ""}
then
    return
end
""")

    for k, v in infos.items():
        f.write(f"""
lib:addInstance(
    {k},
    {to_string(v, level=1)}
)""")

if args.version == 4:
    groups = {}
    read_dungeon_groups(args.version)
    with open(f"instances/groups.lua", "w") as f:
        f.write('local lib = LibStub("LibInstances")')
        for k, v in groups.items():
            f.write(f"\nlib:addGroup({to_string(k)}, {to_string(v)})")

print("instances.lua written...")
