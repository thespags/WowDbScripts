import requests
import json
import re
import logging
from lxml import html
from collections import OrderedDict
from packaging.version import parse as parse_version
from os.path import exists
from pathlib import Path

ignored_zones = {631, 632, 658, 668, 724}
ignored_sort = {"encounters", "activities"}
expansions = {1: "classic", 2: "tbc", 3: "wotlk"}


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
    try:
        with open(file_name) as file:
            return file.read()
    except FileNotFoundError:
        print(f'No {file_name} using default.')
        return default


def write_file_value(file_name, value):
    with open(file_name, "w") as file:
        file.write(value)


def update_files(args, file_name: str = None, table_names: [str] = None):
    if file_name:
        with open(file_name) as file:
            table_names = file.read().splitlines()

    version_file = f'{args.version}/versions'
    if not args.download:
        logging.info("Download set to false, skipping: %s", table_names)
        return
    new_version = get_latest_version(args.version)
    Path(str(args.version)).mkdir(parents=True, exist_ok=True)

    old_version = read_file_value(version_file, "")
    write_file_value(version_file, new_version)

    logging.info(f'Version new: {new_version}, old: {old_version}')

    for table_name in table_names:
        file_name = f'{args.version}/{table_name}.csv'
        if new_version == old_version and exists(file_name):
            if args.force_download:
                logging.info(f'Versions matched and file exists, forcing download: {file_name}')
            else:
                logging.info(f'Versions matched and file exists, skipping download: {file_name}')
                continue
        else:
            logging.info("Missing or out of date file, downloading table: " + file_name)
        url = f'https://wago.tools/db2/{table_name}/csv?build={new_version}'
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_name, "wb") as f:
                f.write(response.content)


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
        if len(v) == 0:
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
        if len(v) == 0:
            return "{}"
        if sort:
            v.sort()
        return "{ " + ", ".join(map(lambda x: to_string(x, sort=sort), v)) + " }"
    elif type(v) is str:
        return "nil" if v == "nil" else f'"{v}"'
    elif type(v) is bool:
        return "true" if v else "false"
    else:
        return str(v)


def get_wow_head_spell_as_tree(expansion, spell_id):
    name = expansions.get(expansion, "")
    url = f'https://www.wowhead.com/{name}/spell={spell_id}'
    response = requests.get(url)
    return url, html.fromstring(response.content)


# If we did an update and the ids are out of order, fix them.
def resort(name, regex, prefix):
    id_to_lines = OrderedDict()
    with open(name) as file:
        for line in file.readlines():
            match = re.match(regex, line)
            if match:
                line_id = int(match.group(1))
                if line_id not in id_to_lines:
                    id_to_lines[line_id] = []
                # Strip to handle any new lines consistently.
                id_to_lines[line_id].append(line.strip())

    with open(name, "w") as file:
        file.write(prefix)
        for _, lines in sorted(id_to_lines.items()):
            for line in lines:
                file.write("\n" + line)
