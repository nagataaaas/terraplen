from terraplen.utils import find_number
from terraplen import Country
from terraplen import Scraper
import pytest

DoHeavyTest = False


class TestUtil:
    def test_find_number(self):
        assert find_number('43%') == 43
        assert find_number('4,392%') == 4392
        assert find_number('4.3%') == 4.3
        assert find_number('その他307個のオプション') == 307
        with pytest.raises(ValueError):
            find_number('%')


class TestCountry:
    def test_country_name(self):
        countries = [("Australia", "com.au"),
                     ("Brazil", "com.br"),
                     ("Canada", "ca"),
                     ("ChinaMainland", "cn"),
                     ("France", "fr"),
                     ("Germany", "de"),
                     ("India", "in"),
                     ("Italy", "it"),
                     ("Japan", "co.jp"),
                     ("Mexico", "com.mx"),
                     ("Netherlands", "nl"),
                     ("Poland", "pl"),
                     ("SaudiArabia", "sa"),
                     ("Singapore", "sg"),
                     ("Spain", "es"),
                     ("Sweden", "se"),
                     ("Turkey", "com.tr"),
                     ("UnitedArabEmirates", "ae"),
                     ("UnitedKingdom", "co.uk"),
                     ("UnitedStates", "com")]
        for (country_name, value) in countries:
            assert Country(value).name == country_name

        with pytest.raises(ValueError):
            Country("Atlantis")
        with pytest.raises(ValueError):
            Country("at")

        assert len(countries) == len(Country)

        if __name__ == '__main__':
            pytest.main()


class TestScraper:

    scraper = Scraper(Country.Japan)
    test_asin = 'B07WXL5YPW'

    def test_domain(self):
        if not DoHeavyTest:
            return
        for country in Country:
            Scraper(country, False).init()

    def test_aa(self):
        pass
