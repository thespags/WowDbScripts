import argparse
import csv
from util import *

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
parser.add_argument("-fd", "--force_download", default=False, action=argparse.BooleanOptionalAction)
args = parser.parse_args()
args.version = 3

update_files(args, table_names=["SpellEffect", "SpellItemEnchantment", "SpellEquippedItems"])

spells_to_effects = {}
with open("3/SpellEffect.csv") as file:
    row: dict[str, str]
    for row in csv.DictReader(file, delimiter=','):
        effect = int(row['Effect'])
        spell_id = int(row['SpellID'])
        if effect == 53:
            spells_to_effects[spell_id] = int(row['EffectMiscValue_0'])


def get_bits(x):
    i = 0
    bits = []
    while pow(2, i) <= x:
        if x & pow(2, i):
            bits.append(i)
        i += 1
    return bits


spells_to_slots = {}
with open("3/SpellEquippedItems.csv") as file:
    row: dict[str, str]
    for row in csv.DictReader(file, delimiter=','):
        spell_id = int(row['SpellID'])
        item_class = int(row['EquippedItemClass'])
        if spell_id in spells_to_effects:
            inv_types = int(row['EquippedItemInvTypes'])
            slots = get_bits(inv_types)
            # Because cloaks are slot 15 not 16...
            slots = [15 if item == 16 else item for item in slots]
            spells_to_slots[spell_id] = slots
            if not slots:
                if item_class == 2:
                    slots.append(16)
                elif item_class == 4:
                    slots.append(17)


with open(f'foo.lua', "w") as file:
    for spell_id, effect_id in spells_to_effects.items():
        if spell_id in spells_to_slots:
            slots = spells_to_slots[spell_id]
            file.write(f'\naddEnchant({spell_id}, {effect_id}, {{{",".join(map(str, slots))}}})')

