# WowDbScripts
Downloads CSV from https://wago.tools/db2/ and scrapes data from https://www.wowhead.com/.

The scripts will aggregate information across multiple CSV's and from WowHead to create Lua files.

## Usage
Creates instance information for a private library.
`python3 instances_scraper.py`

Creates trade skill recipe, spell, item information for a public library.
`python3 recipes_scraper.py {version} {update}`
where version is any major version from [Wago Db](https://wago.tools/db2/) and update is `True` or `False`, default `False`.

Example:  
Downloads all classic Wow information.  
`python3 recipes_scraper.py 1`  

Updates any new information in classic Wow.
`python3 recipes_scraper.py 1 True`

## Utility
Provides some utility in [util.py](util.py).
* Gets latest version of an expansion from [Wago Db](https://wago.tools/db2/).
  * Stores result in a `versions` file that is used to check if a new download is needed
* Downloads a specific database file that is stored by expansion.
* Read/Write a single value to file for later.
* Output Python values as Lua values.
  * Sorts table keys by default, can be disabled.
  * Currently hard codes ignored output and ignored sort.
