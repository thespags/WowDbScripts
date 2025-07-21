from enchant_scraper import write_enchantments
from recipes_scraper import scrape
from recipe_expansion_scraper import scrape_expansions
from util import *


args = parse_args()
scrape_expansions(args)
for expansion in range(1, 11):
    if 5 < expansion < 10:
        continue
    args.version = expansion
    write_enchantments(args)
    scrape(args)
