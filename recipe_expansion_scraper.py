import csv
from util import *
from recipes_scraper import read_skill_lines


def scrape_expansions(args):
    i = 0
    f = open("recipes/expansions.lua", "w")
    write_header(f)
    known_skills = {}
    known_spells = set()
    for expansion in range(1, 11):
        if CLASSIC_EXPANSION < expansion < 7:
            continue
        args.version = expansion
        update_files(args, table_names=["SkillLine", "SkillLineAbility"])
        skills = read_skill_lines(expansion)

        with read_table(expansion, "SkillLineAbility") as file:
            row: dict[str, str]
            for row in csv.DictReader(file, delimiter=','):
                skill_line = int(row["SkillLine"])
                if skill_line not in skills:
                    continue

                spell_id = int(row["Spell"])
                skill_id = int(row["ID"])
                old_spell_id = known_skills.get(skill_id, False)
                if old_spell_id or spell_id in known_spells:
                    # Double check blizzard didn't reuse a skill id.
                    if old_spell_id != spell_id:
                        logging.debug("Change spell id %s: %s != %s", skill_id, old_spell_id, spell_id)
                    continue
                known_skills[skill_id] = spell_id
                known_spells.add(spell_id)
                comment = f'-- {skill_id}'
                f.write(f'\nlib:AddExpansion({spell_id}, {expansion - 1}) {comment}')
                i += 1
    logging.info(f'Scraped {i} recipes over all expansions...')


if __name__ == '__main__':
    scrape_expansions(parse_args())
