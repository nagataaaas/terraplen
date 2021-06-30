from terraplen.utils import find_number, remove_whitespace, thumb_size
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

    def test_remove_whitespace(self):
        assert remove_whitespace('    \t\t  \n') == ''
        assert remove_whitespace('      lonely...       ') == 'lonely...'

    def test_thumb_size(self):
        assert thumb_size('https://m.media-amazon.com/images/I/81jPsqOAU6S.SX38_SY50_CR,0,0,38,50_BG85,85,85_BR-120_PKdp-play-icon-overlay__.png') == (38, 50)
        assert thumb_size('https://m.media-amazon.com/images/I/81jPsqOAU6S.SX380_SY500_CR,0,0,38,50_BG85,85,85_BR-120_PKdp-play-icon-overlay__.png') == (380, 500)


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


if __name__ == '__main__':
    pytest.main()
