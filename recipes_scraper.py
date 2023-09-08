import csv
from util import *
import re
import time
import sys


def read_spell_item_enchantment(version):
    f = open("recipes/{0}/enchantments.lua".format(version), "w")
    with open("{0}/SpellItemEnchantment.csv".format(version)) as file:
        csvreader = csv.reader(file)
        header = next(csvreader)

        for row in csvreader:
            f.write("lib:AddEnchantment({0}, \"{1}\")\n".format(int(row[0]), row[1]))
    f.close()


def get_or_none(value):
    return next(iter(value), None)


def get_recipes(tree):
    script = str(tree.xpath('//script[@type="text/javascript"]/text()')[-1]).split("\n")
    for line in script:
        taught = line.startswith("new Listview({template: 'item', id: 'taught-by-item'")
        if taught:
            return re.findall(r'"classs":9,(?:"\w+":"?\w+"?,)*"id":(\d+)', line)
    return ["nil"]


def get_effect(tree):
    effects = tree.xpath('//th[text()[contains(.,"Effect")]]/../td/span/following-sibling::text()[1]')
    for effect in effects:
        match = re.search("\\((\\d+)\\)", effect)
        if match:
            return match.group(1)
    return "nil"


def read_skill_lines(version):
    skills = set()
    # We use the "can link" column which isn't available until Wotlk.
    # Wotlk skills are a superset of Vanilla and TBC so this should be okay.
    version = version if version >= 3 else 3
    update_files(version, "SkillLine")
    with open("{0}/SkillLine.csv".format(version)) as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        category_index = get_key(header, "CategoryID")
        skill_index = get_key(header, "ID")
        can_link_index = get_key(header, "CanLink")

        categories = {9, 11}
        for row in csvreader:
            category = int(row[category_index])
            can_link = int(row[can_link_index])
            if category not in categories or can_link != 1:
                continue
            skills.add(int(row[skill_index]))
    return skills


def read_spells(version):
    spell_ids = set()
    with open("recipes/{0}/items.lua".format(version)) as file:
        file.readline()
        for line in file.readlines():
            spell_id = int(re.search("lib:\\w+\\(\\d+, (?:\\d+|nil), (\\d+)", line).group(1))
            spell_ids.add(spell_id)
    return spell_ids


def read_skills(version, update):
    skills = read_skill_lines(version)
    f = open("recipes/{0}/items.lua".format(version), "a")
    i = 0
    start_time = time.time()
    global last_skill_id
    last_skill_id = int(read_file_value("recipes/{0}/items-last".format(version), 0))
    print("Update true, Scanning all." if update else "Update false, appending from {0}".format(last_skill_id))
    expansion = expansions.get(version)
    spell_ids = read_spells(version) if update else set()

    if last_skill_id == 0:
        f.write('local lib = LibStub("LibTradeSkillRecipes")\n')

    with open("{0}/SkillLineAbility.csv".format(version)) as file:
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
            i += 1
            if not update and last_skill_id >= skill_id:
                continue
            if spell_id in spell_ids:
                continue
            url = "https://www.wowhead.com/{0}/spell={1}".format(expansion, spell_id)
            if i % 10 == 0:
                print("{0} {1}".format(i, time.time() - start_time))
            response = requests.get(url)
            tree = html.fromstring(response.content)
            name = get_or_none(tree.xpath('//head/meta[@property="twitter:title"]/@content'))
            comment = "-- {0} {1}".format(skill_id, name)
            item_link = get_or_none(tree.xpath('(//th[@id="icontab-icon1"])[1]/../td/span/a/@href'))
            if not item_link:
                effect_id = get_effect(tree)
                if effect_id != "nil":
                    recipes = get_recipes(tree)
                    if len(recipes) >= 2:
                        print("Double recipe: {0} {1}".format(spell_id, comment))
                    for recipe_id in recipes:
                        f.write("lib:AddEnchantmentRecipe({0}, {1}, {2}, {3}) {4}\n"
                                .format(skill_line, recipe_id, spell_id, effect_id, comment))
                last_skill_id = skill_id
                continue
            item_id = re.search("item=(\\d+)", item_link).group(1)

            effects = tree.xpath('//span[text()[contains(.,"Use:")]]/a/@href')
            item_spell_id = "nil"
            effect_id = "nil"
            for effect in effects:
                match = re.search("spell=(\\d+)", effect)
                if match:
                    item_spell_id = match.group(1)
                    effect_url = "https://www.wowhead.com/{0}/spell={1}".format(expansion, item_spell_id)
                    effect_response = requests.get(effect_url)
                    effect_tree = html.fromstring(effect_response.content)
                    effect_id = get_effect(effect_tree)
                    break

            # Gets a recipe if this is from an item versus an NPC
            recipes = get_recipes(tree)
            if len(recipes) > 2:
                print("Double recipe: {0} {1}".format(spell_id, comment))
            for recipe_id in recipes:
                f.write("lib:AddRecipe({0}, {1}, {2}, {3}, {4}, {5}) {6}\n"
                        .format(skill_line, recipe_id, spell_id, item_id, item_spell_id, effect_id, comment))
            last_skill_id = skill_id
    print(i)


def scrape(version, update):
    try:
        expansion = expansions.get(version) if len(expansions.get(version)) > 0 else "retail"
        print("Scraping " + expansion)
        update_files(version, "SkillLine", "SkillLineAbility", "SpellItemEnchantment")
        Path("recipes/{0}".format(version)).mkdir(parents=True, exist_ok=True)
        read_spell_item_enchantment(version)
        read_skills(version, update)
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    except ConnectionError:
        print("Connection Error")
    write_file_value("recipes/{0}/items-last".format(version), str(last_skill_id))
    print("Last Skill Line Id: {0}".format(last_skill_id))
    sys.exit(0)


global last_skill_id
expansions = {1: "classic", 2: "tbc", 3: "wotlk", 10: ""}

update = bool(sys.argv[2]) if len(sys.argv) == 3 else False
scrape(int(sys.argv[1]), update)
