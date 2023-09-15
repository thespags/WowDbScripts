import csv
import time
import argparse
from util import *
from threading import *
from concurrent.futures import ThreadPoolExecutor
from operator import countOf


def read_spell_item_enchantment(version):
    f = open("recipes/{0}/enchantments.lua".format(version), "w")
    f.write('local lib = LibStub("LibTradeSkillRecipes")\n')
    with open("{0}/SpellItemEnchantment.csv".format(version)) as file:
        csvreader = csv.reader(file)
        _ = next(csvreader)

        for row in csvreader:
            f.write("\nlib:AddEnchantment({0}, \"{1}\")".format(int(row[0]), row[1]))
    f.close()


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
                print("Recipes expected but regex not working:\n{0}".format(line))
        creates = line.startswith("new Listview({template: 'spell', id: 'recipes'")
        if creates:
            match = re.search(r'"creates":\[(\d+),', line)
            if match:
                item_id = match.group(1)
    return recipes, item_id


def join_list(strings):
    new_strings = []
    new_string = ""
    for string in strings:
        if string.isspace():
            if len(new_string) > 0:
                new_strings.append(new_string)
                new_string = ""
        else:
            new_string = new_string + string
    if len(new_string) > 0:
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


def read_skill_lines(version, download, force):
    skills = set()
    # We use the "can link" column which isn't available until Wotlk.
    # Wotlk skills are a superset of Vanilla and TBC so this should be okay.
    version = version if version >= 3 else 3
    update_files(version, download, force, "SkillLine")
    with open("{0}/SkillLine.csv".format(version)) as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        category_index = get_key(header, "CategoryID")
        skill_index = get_key(header, "ID")
        # name_index = get_key(header, "DisplayName_lang")
        can_link_index = get_key(header, "CanLink")

        categories = {9, 11}
        for row in csvreader:
            category = int(row[category_index])
            can_link = int(row[can_link_index])
            skill_id = int(row[skill_index])
            if category not in categories or skill_id == 2870:
                continue
            # Secondary Professions must be linkable.
            if category == 9 and can_link != 1:
                continue
            # name = row[name_index]
            skills.add(skill_id)
    return skills


def read_spells(version, file_name, regex):
    spell_ids = set()
    with open("recipes/{0}/{1}".format(version, file_name)) as file:
        for line in file.readlines():
            match = re.search(regex, line)
            if match:
                spell_ids.add(int(match.group(1)))
    return spell_ids


def increment():
    global counter
    counter += 1
    if counter % 100 == 0:
        print("{0} {1:.2f}".format(counter, time.time() - start_time))


def read_skill(args, skills, skill_line, skill_id, spell_ids, spell_id, ignored_ids, f, ignored_file):
    if skill_line not in skills:
        return
    if spell_id in spell_ids or spell_id in ignored_ids:
        with lock:
            increment()
        return
    url, tree = get_wow_head_spell_as_tree(args.version, spell_id)
    name = get_or_none(tree.xpath('//head/meta[@property="twitter:title"]/@content'))
    comment = "-- {0} {1}".format(skill_id, name)
    recipes, item_id = get_recipes_and_item(tree)
    # if len(recipes) >= 2:
    #     print("Double recipe: {0} {1}".format(spell_id, comment))
    if not item_id:
        values = get_effect(url, tree)
        if values["enchant_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write("\nlib:AddEnchantmentRecipe({0}, {1}, {2}, {3}) {4}"
                            .format(skill_line, recipe_id, spell_id, values["enchant_id"], comment))
        elif values["item_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write("\nlib:AddRecipe({0}, {1}, {2}, {3}, nil, nil) {4}"
                            .format(skill_line, recipe_id, spell_id, values["item_id"], comment))
        elif values["salvage_id"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write("\nlib:AddSalvageRecipe({0}, {1}, {2}, {3}) {4}"
                            .format(skill_line, recipe_id, spell_id, values["salvage_id"], comment))
        elif values["crafting_data"]:
            with lock:
                increment()
                for recipe_id in recipes:
                    f.write("\nlib:AddCraftingDataRecipe({0}, {1}, {2}, {3}) {4}"
                            .format(skill_line, recipe_id, spell_id, values["crafting_data"], comment))
        else:
            with lock:
                increment()
                does_not_exist = get_or_none(tree.xpath('//script[@id="data.listPage.notFoundPath"]')) is not None
                on_ptr = get_or_none(tree.xpath('//*[text()[contains(.,"Did You Mean...")]]')) is not None
                extra = "ptr" if on_ptr else "removed" if does_not_exist else ""
                ignored_file.write("\n{0} {1} {2}".format(spell_id, comment, extra))
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
            f.write("\nlib:AddRecipe({0}, {1}, {2}, {3}, {4}, {5}) {6}"
                    .format(skill_line, recipe_id, spell_id, item_id, item_spell_id, enchant_id, comment))


def read_skills(args):
    skills = read_skill_lines(args.version, args.download, args.force_download)
    f = open("recipes/{0}/items.lua".format(args.version), "a")
    ignored_file = open("recipes/{0}/ignored".format(args.version), "a")
    spell_ids = read_spells(args.version, "items.lua", r'lib:\w+\(\d+, (?:\d+|nil), (\d+)')
    ignored_ids = read_spells(args.version, "ignored", r'(\d+) --')
    skill_ids = read_spells(args.version, "items.lua", r'lib:\w+\([\w, ]+\) -- (\d+) [\w: ]+')
    last_skill_id = max(skill_ids, default=0)
    print("Updating {0:.2f}...".format(time.time() - start_time))
    if last_skill_id == 0:
        f.write('local lib = LibStub("LibTradeSkillRecipes")\n')

    with open("{0}/SkillLineAbility.csv".format(args.version)) as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        skill_line_index = get_key(header, "SkillLine")
        id_index = get_key(header, "ID")
        spell_id_index = get_key(header, "Spell")
        threads = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            for row in csvreader:
                skill_line = int(row[skill_line_index])
                spell_id = int(row[spell_id_index])
                skill_id = int(row[id_index])
                future = executor.submit(read_skill, args, skills, skill_line, skill_id, spell_ids, spell_id, ignored_ids, f, ignored_file)
                threads.append(future)
        for thread in threads:
            thread.result()
        f.close()
        ignored_file.close()
    print("{0} {1:.2f}".format(counter, time.time() - start_time))


def scrape():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int)
    parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-fd", "--force-download", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-f", "--force", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-e", "--expansions", default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    # Create one massive expansion map every scrape.
    if args.expansions:
        scrape_expansions(args)

    # For the specific expansions get spells and enchantments.
    if args.version:
        print("Scraping {0}".format(args.version))
        if args.force:
            print("Force selected, deleting old files.")
            Path("recipes/{0}/ignored".format(args.version)).unlink()
            Path("recipes/{0}/items.lua".format(args.version)).unlink()

        update_files(args.version, args.download, args.force_download, "SkillLine", "SkillLineAbility", "SpellItemEnchantment")
        Path("recipes/{0}".format(args.version)).mkdir(parents=True, exist_ok=True)
        read_spell_item_enchantment(args.version)
        read_skills(args)

        # Post scrape, fix sorting by db id.
        resort("recipes/{0}/ignored".format(args.version), r'\w+ -- (\w+) .*', "")
        resort("recipes/{0}/items.lua".format(args.version), r'lib:\w+\([\w, ]+\) -- (\w+) .*', LIB_LINE)
        print("Finished sorting {0:.2f}...".format(time.time() - start_time))


def scrape_expansions(args):
    i = 0
    f = open("recipes/expansions.lua", "w")
    f.write(LIB_LINE)
    known = {}

    for expansion in range(1, 11):
        if 3 < expansion < 7:
            continue
        skills = read_skill_lines(expansion, args.download, args.force_download)
        update_files(expansion, args.download, args.force_download, "SkillLineAbility")

        with open("{0}/SkillLineAbility.csv".format(expansion)) as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            skill_line_index = get_key(header, "SkillLine")
            id_index = get_key(header, "ID")
            spell_id_index = get_key(header, "Spell")

            for row in csvreader:
                skill_line = int(row[skill_line_index])
                if skill_line not in skills:
                    continue

                spell_id = int(row[spell_id_index])
                skill_id = int(row[id_index])
                old_spell_id = known.get(skill_id, False)

                if old_spell_id:
                    # if old_spell_id != spell_id:
                    #     print("changed spell id {0}: {1} != {2}".format(skill_id, old_spell_id, spell_id))
                    continue
                known[skill_id] = spell_id
                comment = "-- {0}".format(skill_id)
                f.write("\nlib:AddExpansion({0}, {1}) {2}".format(spell_id, expansion - 1, comment))
                i += 1
    print(i)


lock = Lock()
start_time = time.time()
counter = 0
LIB_LINE = 'local lib = LibStub("LibTradeSkillRecipes")\n'
scrape()
