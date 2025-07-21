# WowDbScripts
Downloads CSV from https://wago.tools/db2/ and scrapes data from https://www.wowhead.com/.

The scripts will aggregate information across multiple CSV's and from WowHead to create Lua files.

## Setup
This repo is set up for python 3.11.x but may work on other versions of python.
To configure your environment,
```bash
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
If you add new python modules, then
```bash
pip freeze > requirements.txt
```

## Usage
Creates instance information for a private library.
`python3 instances_scraper.py`

Example:  
Scrapes Woltk instance information with existing files
`python3 instances_scraper.py`

Updates any new information in classic Wow.
`python3 instances_scraper.py -d`

Force download tables. (Sometimes Blizzard updates tables without version changes)
`python3 instances_scraper.py -d -fd`

We have a combination of scrapers to create LibTradeSkillRecipes for expansions on [Wago Db](https://wago.tools/db2/).
* `recipes_scraper.py` 
  * Creates trade skill recipe, spell, item information
* `recipe_expansion_scraper.py`
  * Collects the information was initially added (does not track if it was removed)
* `enchant_scrapper.py`
  * Gets the effect and slot information for an enchant across all languages
  * The Wow API does not provide language support for effects.
* `all_scrapper.py`
  * Calls the other three scrapers across all expansions.

Example (supports versions 1, 2, 3, 4, 5 and 10):  

Scrapes all classic Wow information with existing files (offline mode)
`python3 recipes_scraper.py -v 1`  

Updates any new information in classic Wow.
`python3 recipes_scraper.py -v 1 -d`

Force download tables. (Sometimes Blizzard updates tables without version changes)
`python3 recipes_scraper.py -v 1 -d -fd`

By default, we overwrite any output. `items.lua` and `ignored` are not updated unless `-fd` is provided 
as these are most intensive to collect so by default appends.

For `all_scraper.py`, this does not use version but will accept `d` and `-fd` for downloading.

e.g. `python3 all_scrapper.py -d` will update all files when updating LibTradeSkillRecipes.

## Utility
Provides some utility in [util.py](util.py).
* Gets latest version of an expansion from [Wago Db](https://wago.tools/db2/).
  * Stores result in a `versions` file that is used to check if a new download is needed
* Downloads a specific database file that is stored by expansion.
* Read/Write a single value to file for later.
* Output Python values as Lua values.
  * Sorts table keys by default, can be disabled.
  * Currently hard codes ignored output and ignored sort.
