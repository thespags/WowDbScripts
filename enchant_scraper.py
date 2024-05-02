import csv
from util import *


def get_bits(x):
    i = 0
    bits = []
    while pow(2, i) <= x:
        if x & pow(2, i):
            bits.append(i)
        i += 1
    return bits


def get_test_spells(version):
    test_spells = set()
    with read_table(version, "SpellName") as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            name = row['Name_lang']
            spell_id = int(row['ID'])
            if "TEST" in name:
                test_spells.add(spell_id)
    return test_spells


def write_effect_names(version, effect_ids):
    effects = {}
    total = 0
    with open(recipes_lua(version, "effects"), "w") as out:
        write_header(out, version)
        out.write("\nlocal locale = GetLocale()")
        out.write("\nlocale = locale == \"enGB\" and \"enUS\" or locale\n")
        for index, language in enumerate(languages):
            out.write(f"\n{'elseif' if index > 0 else 'if'} locale == \"{language}\" then")
            with read_table(version, "SpellItemEnchantment", language) as file:
                row: dict[str, str]
                for row in csv.DictReader(file, delimiter=','):
                    effect_id = int(row['ID'])
                    if effect_id not in effect_ids:
                        continue
                    name = row['Name_lang']
                    if language == "enUS":
                        effects[effect_id] = name
                    name = name.replace('"', '\\\"')
                    out.write(f'\n\tlib:AddEffect({effect_id}, "{name}")')
                    total += 1
        out.write("\nend")
    logging.info("Scraped %s effects.", total)
    return effects


def add_slots(version, spells):
    with read_table(version, "SpellEquippedItems") as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            spell_id = int(row['SpellID'])
            item_class = int(row['EquippedItemClass'])
            if spell_id in spells:
                inv_types = int(row['EquippedItemInvTypes'])
                slots = get_bits(inv_types)
                # Because cloaks are slot 15 not 16...
                slots = [15 if item == 16 else item for item in slots]
                spells[spell_id]["slots"] = slots
                if not slots:
                    if item_class == 2:
                        slots.append(16)
                    elif item_class == 4:
                        slots.append(17)
                if 20 in slots:
                    slots.remove(20)


def write_enchantments(args):
    update_files(args, table_names=["SpellEffect", "SpellEquippedItems", "SpellName"])
    update_files(args, table_names=["SpellItemEnchantment"], all_languages=True)
    Path(recipes_lua(args.version, "")).mkdir(parents=True, exist_ok=True)
    test_spells = get_test_spells(args.version)
    spells = {}
    effect_ids = set()
    with read_table(args.version, "SpellEffect") as file:
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            effect = int(row['Effect'])
            spell_id = int(row['SpellID'])
            if effect == 53 and spell_id not in test_spells:
                spell = spells.setdefault(spell_id, {})
                effect = int(row['EffectMiscValue_0'])
                effect_ids.add(effect)
                spell["effect"] = effect
    add_slots(args.version, spells)
    effects = write_effect_names(args.version, effect_ids)

    with open(recipes_lua(args.version, "enchantments"), "w") as file:
        write_header(file, args.version)
        for spell_id, spell in sorted(spells.items()):
            slots = ",".join(map(str, spell.get("slots", {})))
            effect_id = spell["effect"]
            file.write(f'\nlib:AddEnchantment({spell_id}, {effect_id}, {{{slots}}}) -- {effects.get(effect_id, "unknown")}')
    logging.info("Scraped %s enchantments.", len(spells))


if __name__ == '__main__':
    write_enchantments(parse_args())
