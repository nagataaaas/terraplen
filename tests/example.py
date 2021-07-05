from terraplen import Scraper

from terraplen.models import *

# I love walking dead! Now I want a Walking Dead Poster for my room...

scraper = Scraper(Country.UnitedStates)

scraper.search('Walking Dead')