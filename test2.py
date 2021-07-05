from terraplen import Scraper
from terraplen.models import Country, Language, Currency
import re
import json
from pprint import pprint

ss = []

sports = []
home = []
toysandgames = []

for c in list(Country.__iter__())[::-1]:
    s = Scraper(c)
    soup = s.search('why')
    for l in soup.select('#searchDropdownBox > option'):
        ss.append([l['value'], l.string])
        if 'sports' in l['value']:
            sports.append(c)
        if 'home-improvement' in l['value']:
            home.append(c)
        if 'toys-and' in l['value']:
            toysandgames.append(c)

print(sports)
print(home)
print(toysandgames)

# 'aps': ['All Departments'],
#      'alexa-skills': ['Alexa Skill'],
#      'amazon-devices': ['Amazon Device'],
#      'amazon-global-store': ['Amazon Global Store'],
#      'mobile-apps': ['App And Game'],
#      'audible': ['Audible'],
#      'automotive': ['Automotive'],
#      'baby': ['Baby'],
#      'beauty': ['Beauty'],
#      'stripbooks': ['Book'],
#      'popular': ['CDs And Vinyl'],
#      'fashion': ['Fashion'],
#      'fashion-womens': ['FashionWomen'],
#      'fashion-mens': ['FashionMen'],
#      'fashion-girls': ['FashionGirl'], 'fashion-boys': ['Boy'],
#      'fashion-baby': ['FashionBaby'],
#      'warehouse-deals': ['Amazon Warehouse'],
#      'computers': ['Computer'],
#      'electronics': ['Electronic'],
#      'garden': ['Garden'],
#      'gift-cards': ['Gift Card'],
#      'hpc': ['Health'],
#      'home': ['Home'],
#      'home-improvement': ['HomeImprovement'],
#      'digital-text': ['Kindle Store'],
#      'kitchen': ['Kitchen And Dining'],
#      'fashion-luggage': ['Luggage And Travel Gear'],
#      'movies-tv': ['Movie And TV'],
#      'mi': ['Musical Instrument'],
