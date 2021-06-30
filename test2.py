from terraplen import Scraper, Country, Language, Currency
import re
import json
from pprint import pprint

# #aod-end-of-results
asin = 'B07RPQRPR5'  # chokinbako twisting
asin = 'B08GG1QSRR'  # DualSense twisting
asin = 'B084G2VWFW'  # backpack not twisting
asin = 'B097XB91KH'  # book single
asin = 'B00GRKD6XU'  # book twisting kindle
asin = '4798121967'  # book twisting
asin = 'B07HJ52LKD'  # chokinbako not twisting
asin = 'B09319VMGT'  # tales-of-arise twisting video

s = Scraper(Country.Japan, currency=Currency.CanadianDollar, language=Language.Malayalam)
d = s.get_product(asin)
pprint(d)
# for img in d.images:
#     print(img.largest_image)
exit()
print(s.get_offers(asin, page=1).offers)
print(s.get_offers(asin, page=2).offers)
print(s.get_review(asin))
print(s.get_rating(asin))
print(s.cookie)
print(s.currency, s.language)
