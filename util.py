import requests
import json
from lxml import html
from packaging.version import parse as parse_version
from os.path import exists
from pathlib import Path


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


def update_files(major, *files):
    new_version = get_latest_version(major)
    Path(str(major)).mkdir(parents=True, exist_ok=True)

    file_name = "{0}/versions".format(major)
    old_version = read_file_value(file_name, "")
    write_file_value(file_name, new_version)

    print("Version new: {0}, old: {1}".format(new_version, old_version))

    for file in files:
        file_name = "{0}/{1}.csv".format(major, file)
        if new_version == old_version and exists(file_name):
            print("Versions matched and file exists, skipping download: " + file_name)
            continue
        print("Downloading file: " + file_name)
        url = "https://wago.tools/db2/{0}/csv?build={1}".format(file, new_version)
        response = requests.get(url)
        open(file_name, "wb").write(response.content)


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


ignored_zones = {631, 632, 658, 668, 724}
ignored_sort = {"encounters"}


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
            sort = key not in ignored_sort
            comment = "--" if ignore or ignored else ""
            output += "{0}{1}{2} = {3},".format(
                indent,
                comment,
                key_string(v=key),
                to_string(v=v[key], level=level+1, ignore=ignored, sort=sort),
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
        return "\"{0}\"".format(v)
    elif type(v) is bool:
        return "true" if v else "false"
    else:
        return str(v)