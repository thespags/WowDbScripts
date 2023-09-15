import requests
import json
import re
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
        f = open(file_name, "r")
        value = f.read()
        f.close()
        return value
    except FileNotFoundError:
        print("No {0} using default.".format(file_name))
        return default


def write_file_value(file_name, value):
    f = open(file_name, "w")
    f.write(value)
    f.close()


def update_files(expansion: object, download: bool, force: bool, *table_names: object):
    version_file = "{0}/versions".format(expansion)
    if not download:
        print("Skipping Update " + version_file)
        return
    new_version = get_latest_version(expansion)
    Path(str(expansion)).mkdir(parents=True, exist_ok=True)

    old_version = read_file_value(version_file, "")
    write_file_value(version_file, new_version)

    print("Version new: {0}, old: {1}".format(new_version, old_version))

    for table_name in table_names:
        file_name = "{0}/{1}.csv".format(expansion, table_name)
        if new_version == old_version and exists(file_name):
            if force:
                print("Versions matched and file exists, forcing download: " + file_name)
            else:
                print("Versions matched and file exists, skipping download: " + file_name)
                continue
        else:
            print("Missing or out of date file, downloading table: " + file_name)
        url = "https://wago.tools/db2/{0}/csv?build={1}".format(table_name, new_version)
        response = requests.get(url)
        with open(file_name, "wb") as f:
            f.write(response.content)


def get_key(header, value):
    for i, x in enumerate(header):
        if x == value:
            return i
    raise Exception("value doesn't exist")


def key_string(v):
    if type(v) is str:
        return str(v)
    elif type(v) is int:
        return "[{0}]".format(v)
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
        return "nil" if v == "nil" else "\"{0}\"".format(v)
    elif type(v) is bool:
        return "true" if v else "false"
    else:
        return str(v)


def get_wow_head_spell_as_tree(expansion, spell_id):
    name = expansions.get(expansion, "")
    url = "https://www.wowhead.com/{0}/spell={1}".format(name, spell_id)
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
