from terraplen import Scraper

from terraplen.models import *

# I love walking dead! Now I want a Walking Dead Poster for my room...

scraper = Scraper(Country.Japan)

print(scraper.search('充電ケーブル', merchant='amazon'))
