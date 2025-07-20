import requests
import json
import re
import logging
import argparse
from lxml import html
from collections import OrderedDict
from packaging.version import parse as parse_version
from os.path import exists
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
logging.basicConfig(format='%(message)s', level=logging.INFO)
ignored_zones = {}
ignored_sort = {"encounters", "activities"}
expansions = {1: "classic", 2: "tbc", 3: "wotlk", 4: "cata", 5: "mop-classic"}
languages = ["enUS", "deDE", "esES", "esMX", "frFR", "itIT", "koKR", "ptBR", "ruRU", "zhCN", "zhTW"]


def write_header(file, version=None):
    file.write('local lib = LibStub("LibTradeSkillRecipes-1")\n')
    if version:
        file.write(f"\nif {version - 1} ~= LE_EXPANSION_LEVEL_CURRENT then\n\treturn\nend")


def get_latest_version(major):
    url = "https://wago.tools/db2"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    data = tree.xpath('//div[@id="app"]//@data-page')[0]
    json_object = json.loads(data)
    # print(json.dumps(json_object, indent=2))
    for v in json_object["props"]["versions"]:
        if parse_version(v).major == major:
            return v


def read_file_value(file_name, default):
    path = Path(file_name)
    if path.exists():
        with path.open() as file:
            return file.read()
    else:
        print(f'No {file_name} using default.')
        return default


def write_file_value(file_name, value):
    with open(file_name, "w") as file:
        file.write(value)


def get_table(version, table_name, language="enUS"):
    return f"{version}/{table_name}-{language}.csv"


def read_table(version, table_name, language="enUS"):
    return open(get_table(version, table_name, language), encoding='utf-8')


def recipes_lua(version, file_name):
    suffix = ".lua" if file_name not in ("ignored", "") else ""
    return f"recipes/{version}/{file_name}{suffix}"


def update_file(file_name, url):
    response = requests.get(url)
    response.raise_for_status()
    with open(file_name, "wb") as f:
        f.write(response.content)


def update_files(args, table_names: [str] = None, all_languages=False):
    table_names = table_names if table_names else []
    version_file = f'{args.version}/versions'
    if not args.download:
        logging.info("Download set to false, skipping: %s", table_names)
        return
    new_version = get_latest_version(args.version)
    Path(str(args.version)).mkdir(parents=True, exist_ok=True)

    old_version = read_file_value(version_file, "")
    write_file_value(version_file, new_version)

    logging.info(f'Version new: {new_version}, old: {old_version}')

    threads = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        for table_name in table_names:
            for language in languages if all_languages else ["enUS"]:
                file_name = get_table(args.version, table_name, language)
                if new_version == old_version and exists(file_name):
                    if args.force_download:
                        logging.info(f"Versions matched and file exists, forcing download: {file_name}")
                    else:
                        logging.info(f"Versions matched and file exists, skipping download: {file_name}")
                        continue
                else:
                    logging.info("Missing or out of date file, downloading table: " + file_name)
                url = f"https://wago.tools/db2/{table_name}/csv?build={new_version}&locale={language}"
                future = executor.submit(update_file, file_name, url)
                threads.append(future)
    for thread in threads:
        thread.result()


def key_string(v):
    if type(v) is str:
        return str(v)
    elif type(v) is int:
        return f'[{v}]'
    else:
        raise Exception("unknown key type")


# A complicated thing of sorting and new lines to print a python map as a lua map.
# Some things we want sorted for readability, map keys, number lists.
# Other things we don't want sorted like encounter order.
def to_string(v, level=0, ignore=False, sort=True):
    if type(v) is dict:
        if not len(v):
            return "{}"
        newline = level == 0 or level == 1
        indent = "\n" + "    " * (level + 1) if newline else " "
        keys = list(v.keys())
        keys.sort()
        output = "{"
        for key in keys:
            ignored = key in ignored_zones
            key_sort = sort and key not in ignored_sort
            comment = "--" if ignore or ignored else ""
            output += "{0}{1}{2} = {3},".format(
                indent,
                comment,
                key_string(v=key),
                to_string(v=v[key], level=level+1, ignore=ignored, sort=key_sort),
            )
        comment = "--" if ignore else ""
        output += "\n" + "    " * level + comment + "}" if newline else " }"
        return output
    elif type(v) is set:
        return to_string(list(v), sort=sort)
    elif type(v) is list:
        if not len(v):
            return "{}"
        if sort:
            v.sort()
        return "{ " + ", ".join(map(lambda x: to_string(x, sort=sort), v)) + " }"
    elif type(v) is str:
        return "nil" if v == "nil" else f'{json.dumps(v)}'
    elif type(v) is bool:
        return "true" if v else "false"
    else:
        return str(v)


def get_wow_head_spell_as_tree(expansion, spell_id):
    name = expansions.get(expansion, "")

    url = f'https://www.wowhead.com/{name}/spell={spell_id}'
    print(url)
    response = requests.get(url)
    return html.fromstring(response.content)


# If we did an update and the ids are out of order, fix them.
def resort(name, regex):
    id_to_lines = OrderedDict()
    prefix = []
    with open(name) as file:
        for line in file.readlines():
            match = re.match(regex, line)
            if match:
                line_id = int(match.group(1))
                if line_id not in id_to_lines:
                    id_to_lines[line_id] = []
                # Strip to handle any new lines consistently.
                id_to_lines[line_id].append(line.strip())
            else:
                prefix.append(line)

    with open(name, "w") as file:
        file.write("".join(prefix).strip())
        for _, lines in sorted(id_to_lines.items()):
            for line in lines:
                file.write("\n" + line)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int)
    parser.add_argument("-d", "--download", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-fd", "--force-download", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("-f", "--force", default=False, action=argparse.BooleanOptionalAction)
    return parser.parse_args()
