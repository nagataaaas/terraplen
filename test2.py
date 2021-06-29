from terraplen import Scraper, Country, Language, Currency
import re
import json
from pprint import pprint

# #aod-end-of-results
asin = 'B08GG1QSRR'
asin = 'B084G2VWFW'
asin = 'B07RPQRPR5'
s = Scraper(Country.Japan, currency=Currency.CanadianDollar, language=Language.Malayalam)
s1, s2 = s.get_product(asin)
pprint(json.loads(s1.replace('\n', '').replace(',]', ']').replace(',}', '}')))
# pprint(json.loads(s2.replace('\n', '').replace(',]', ']').replace("'", '"')))
pprint(json.loads(s2.replace('\n', '').replace("'", '"').replace(',]', ']').replace(',}', '}')))
exit()
print(s.get_offers(asin, page=1).offers)
print(s.get_offers(asin, page=2).offers)
print(s.get_review(asin))
print(s.get_rating(asin))
print(s.cookie)
print(s.currency, s.language)
