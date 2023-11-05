import csv
import argparse
from util import *


def scrape_teleports(args):

    update_files(args, table_names=["SpellReagents"])
    teleport_ids = set()
    portal_ids = set()

    with open(f'3/SpellReagents.csv') as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            reagent_id = int(row["Reagent_0"])
            spell_id = int(row["SpellID"])
            if reagent_id == 17031:
                teleport_ids.add(spell_id)
            elif reagent_id == 17032:
                portal_ids.add(spell_id)

    Path("teleports").mkdir(parents=True, exist_ok=True)
    f = open("teleports/spell_ids", "w")
    f.write("local teleportIds = " + to_string(teleport_ids))
    f.write("\nlocal portalIds = " + to_string(portal_ids))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-fd", "--force_download", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()
args.version = 3
scrape_teleports(args)
