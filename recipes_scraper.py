import csv
import time
from util import *
from threading import *
from concurrent.futures import ThreadPoolExecutor
from operator import countOf
lock = Lock()
counter = 0
start_time = 0


def get_or_none(value):
    return next(iter(value), None)


# Viewing the script box seems to be the most consistent on wowhead for getting recieps and any iteams created.
# Previously I tried things in `Effect` but some pages do not have the item information.
def get_recipes_and_item(tree):
    script = str(tree.xpath('//script[@type="text/javascript"]/text()')[-1]).split("\n")
    recipes = ["nil"]
    item_id = None
    for line in script:
        taught = line.startswith("new Listview({template: 'item', id: 'taught-by-item'")
        if taught:
            # [\w.:, "\-\\\'], too many characters to match so just match all within quotes
            recipes = re.findall(r'"classs":\d+,(?:"\w+":(?:\w+|".+?"),)*?"id":(\d+)', line)
            if not recipes:
                logging.error('Recipes expected but regex not working:\n%s', line)
        creates = line.startswith("new Listview({template: 'spell', id: 'recipes'")
        if creates:
            match = re.search(r'"creates":\[(\d+),', line)
            if match:
                item_id = int(match.group(1))
    return recipes, item_id


def join_list(strings):
    new_strings = []
    new_string = ""
    for string in strings:
        if string.isspace():
            if len(new_string):
                new_strings.append(new_string)
                new_string = ""
        else:
            new_string = new_string + string
    if len(new_string):
        new_strings.append(new_string)
    return new_strings


def get_effect(url, tree):
    effects = join_list(tree.xpath('//th[text()[contains(.,"Effect")]]/../td/text()'))
    values = {
        "enchant_id": None,
        "item_id": None,
        "salvage_id": None,
        "crafting_data": None,
    }
    for effect in effects:
        if effect.startswith("Enchant Item") \
                or effect.startswith("Add Socket to Item") \
                or effect.startswith("Apply Enchant Appearance"):
            match = re.search(r"\((\d+)\)", effect)
            if match:
                values["enchant_id"] = match.group(1)
        if effect.startswith("Create Item") or effect.startswith("Create Tradeskill Item"):
            items = get_or_none(tree.xpath('//table[@class="icontab"]/tr/td/span/a/@href')) or ""
            match = re.search(r'item=(\d+)', items)
            if match:
                values["item_id"] = match.group(1)
            else:
                # Cheat to say this creates something but not an item.
                values["item_id"] = "nil"
        # if effect.startswith("Summon Object"):
        #     print(url)
        if effect.startswith("Craft Crafting Data"):
            match = re.search(r"\((\d+)\)", effect)
            if match:
                values["crafting_data"] = match.group(1)
        if effect.startswith("Salvage Item"):
            match = re.search(r"\((\d+)\)", effect)
            if match:
                values["salvage_id"] = match.group(1)
    if countOf(values.values(), None) < 3:
        print(values)
    return values


def read_skill_lines(version):
    skill_lines = {}
    with read_table(version, "SkillLine") as file:
        categories = {9, 11}
        row: dict[str, str]
        for row in csv.DictReader(file, delimiter=','):
            category = int(row["CategoryID"])
            skill_id = int(row["ID"])
            flags = int(row["Flags"])
            # If secondary or primary profession, that appears in the spell book (128), is shown in the ui (not 2),
            # and not automatic (not 16). In case of Jewelcrafting in TBC (755), include because its incorrectly flagged.
            # Ignore logging as well (1945)
            include_skill_line = category in categories and flags & 128 and flags & 18 == 0
            if (include_skill_line or skill_id == 755) and skill_id != 1945:
                name = row["DisplayName_lang"]
                logging.debug("%s %s %s", skill_id, name, str(flags))
                skill_lines[skill_id] = {"name": name, "category": category, "spells": []}

    with read_table(version, "SkillLineAbility") as f:
        for row in csv.DictReader(f, delimiter=','):
            skill_line = int(row['SkillLine'])
            flags = int(row['Flags'])
            supercedes_spell_id = int(row['SupercedesSpell'])
            # Seeds the first supercede then we only add spells that supercede that chain.
            # Assumes ordering is consistent, i.e. supercede chain appears in order in the DB.
            if skill_line in skill_lines and flags == 0 and supercedes_spell_id != 0:
                spells = skill_lines[skill_line]["spells"]
                if not len(spells):
                    spells.append(supercedes_spell_id)
                if supercedes_spell_id == spells[-1]:
                    spell_id = int(row['Spell'])
                    skill_lines[skill_line]["spells"].append(spell_id)
    return skill_lines


def write_skill_lines(version, skill_lines):
    file_name = recipes_lua(version, "skill_lines")
    with open(file_name, "w") as file:
        write_header(file, version)
        for k, v in skill_lines.items():
            file.write(f'\nlib:AddSkillLine({k}, "{v["name"]}", {v["category"]}, {{{",".join(map(str, v["spells"]))}}})')
    resort(file_name, r'lib:\w+\((\d+), .*')


def read_spells(version, file_name, regex):
    spell_ids = set()
    with open(recipes_lua(version, file_name)) as file:
        for line in file.readlines():
            match = re.search(regex, line)
            if match:
                spell_ids.add(int(match.group(1)))
    return spell_ids


def increment():
    global counter
    counter += 1
    if counter % 100 == 0:
        print(f'{counter} {time.time() - start_time:.2f}')


def read_skill(args, row, skill_lines, spell_ids, ignored_ids, f, ignored_file):
    skill_line = int(row["SkillLine"])
    spell_id = int(row["Spell"])
    skill_id = int(row["ID"])
    if skill_line not in skill_lines:
        return
    if spell_id in spell_ids or spell_id in ignored_ids:
        with lock:
            increment()
        return
    url, tree = get_wow_head_spell_as_tree(args.version, spell_id)
    name = get_or_none(tree.xpath('//head/meta[@property="twitter:title"]/@content'))
    comment = f'-- {skill_id} {name}'
    recipes, item_id = get_recipes_and_item(tree)
    if not item_id:
        values = get_effect(url, tree)
        if values["enchant_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write(f'\nlib:AddEnchantmentRecipe({skill_line}, {recipe_id}, {spell_id}, {values["enchant_id"]}) {comment}')
        elif values["item_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write(f'\nlib:AddRecipe({skill_line}, {recipe_id}, {spell_id}, {values["item_id"]}, nil, nil) {comment}')
        elif values["salvage_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write(f'\nlib:AddSalvageRecipe({skill_line}, {recipe_id}, {spell_id}, {values["salvage_id"]}) {comment}')
        elif values["crafting_data"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write(f'\nlib:AddCraftingDataRecipe({skill_line}, {recipe_id}, {spell_id}, {values["crafting_data"]}) {comment}')
        else:
            with lock:
                increment()
                does_not_exist = get_or_none(tree.xpath('//script[@id="data.listPage.notFoundPath"]')) is not None
                on_ptr = get_or_none(tree.xpath('//*[text()[contains(.,"Did You Mean...")]]')) is not None
                extra = "ptr" if on_ptr else "removed" if does_not_exist else ""
                ignored_file.write(f'\n{spell_id} {comment} {extra}')
        return
    effects = tree.xpath('//span[text()[contains(.,"Use:")]]/a/@href')
    item_spell_id = "nil"
    enchant_id = "nil"
    for effect in effects:
        match = re.search("spell=(\\d+)", effect)
        if match:
            item_spell_id = match.group(1)
            url, effect_tree = get_wow_head_spell_as_tree(args.version, item_spell_id)
            values = get_effect(url, effect_tree)
            enchant_id = values["enchant_id"] or "nil"
            break
    with lock:
        increment()
        for recipe_id in recipes:
            f.write(f'\nlib:AddRecipe({skill_line}, {recipe_id}, {spell_id}, {item_id}, {item_spell_id}, {enchant_id}) {comment}')


def read_skills(args):
    skill_lines = read_skill_lines(args.version)
    write_skill_lines(args.version, skill_lines)
    f = open(recipes_lua(args.version, "items"), "a")
    ignored_file = open(recipes_lua(args.version, "ignored"), "a")
    spell_ids = read_spells(args.version, "items", r'lib:\w+\(\d+, (?:\d+|nil), (\d+)')
    ignored_ids = read_spells(args.version, "ignored", r'(\d+) --')
    skill_ids = read_spells(args.version, "items", r'lib:\w+\([\w, ]+\) -- (\d+) [\w: ]+')
    if not len(skill_ids):
        write_header(f, args.version)
    #
    # print(f'Scraping Effects: {time.time() - start_time:.2f}')
    # # Update spell_ids.
    # spell_to_items = {}
    # spell_to_quantity = {}
    # effect_count = 0
    # with open_table(args.version, "SpellEffect") as file:
    #     for row in csv.DictReader(file, delimiter=','):
    #         effect = int(row['Effect'])
    #         spell_id = int(row['SpellID'])
    #         item_id = int(row['EffectItemType'])
    #         if (effect == 24 or effect == 157) and item_id != 0:
    #             spell_to_items[spell_id] = item_id
    #             base_points = int(row['EffectBasePoints'])
    #             bonus_coefficient = int(row['EffectBonusCoefficient'])
    #             group_coefficient = int(row['GroupSizeBasePointsCoefficient'])
    #             spell_to_quantity[spell_id] = base_points + bonus_coefficient + group_coefficient
    #             effect_count += 1
    #         # elif effect == 53:
    #         #     print("spellId {0} {1}".format(spell_id, effect))
    # print(f'Finished Effects: {effect_count} {time.time() - start_time:.2f}')

    print(f'Scraping Spells: {time.time() - start_time:.2f}')
    with read_table(args.version, "SkillLineAbility") as file:
        threads = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            row: dict[str, str]
            for row in csv.DictReader(file, delimiter=','):
                future = executor.submit(read_skill, args, row, skill_lines, spell_ids, ignored_ids, f, ignored_file)
                threads.append(future)
        for thread in threads:
            thread.result()
        f.close()
        ignored_file.close()
    print(f'Finished Spells: {counter} {time.time() - start_time:.2f}')

    # spell_to_reagents = {}
    # with open_table(args.version, "SpellReagents") as file:
    #     for row in csv.DictReader(file, delimiter=','):
    #         spell_id = int(row['SpellID'])
    #         if spell_id in spell_ids:
    #             reagents = {}
    #             for i in range(0, 8):
    #                 reagent_item_id = int(row['Reagent_' + str(i)])
    #                 reagent_quantity = int(row['ReagentCount_' + str(i)])
    #                 if reagent_item_id != 0 and reagent_quantity != 0:
    #                     reagents[reagent_item_id] = reagent_quantity
    #             spell_to_reagents[spell_id] = reagents


def scrape(args):
    global start_time
    start_time = time.time()
    # For the specific expansions get spells and enchantments.
    if args.version:
        print(f'Scraping {args.version}')
        if args.force:
            print("Force selected, deleting old files.")
            Path(recipes_lua(args.version, "ignored")).unlink()
            Path(recipes_lua(args.version, "items")).unlink()

        # Downloads the 4 main tables plus additional tables from the file.
        update_files(args, table_names=["SkillLine", "SkillLineAbility", "SpellItemEnchantment", "SpellEffect"])
        Path(recipes_lua(args.version, "")).mkdir(parents=True, exist_ok=True)
        read_skills(args)

        # Post scrape, fix sorting by db id.
        resort(recipes_lua(args.version, "ignored"), r'\w+ -- (\w+) .*')
        resort(recipes_lua(args.version, "items"), r'lib:\w+\([\w, ]+\) -- (\w+) .*')
        print(f'Finished sorting {time.time() - start_time:.2f}...')


if __name__ == '__main__':
    scrape(parse_args())
