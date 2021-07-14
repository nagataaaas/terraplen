from terraplen.utils import find_number, remove_whitespace, thumb_size, product, parse_asin_from_url
from terraplen.models import Country, Variation, Category, PrimeVideoTV, Product, PrimeVideoMovie, Book, Movie, \
    ProductVariations, Kindle
from terraplen import Scraper
import pytest

DoHeavyTest = True


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
        assert thumb_size('https://m.media-amazon.com/images/I/81jPsqOAU6S.SX38_SY50_CR,0,0,38,50_BG85,'
                          '85,85_BR-120_PKdp-play-icon-overlay__.png') == (38, 50)
        assert thumb_size('https://m.media-amazon.com/images/I/81jPsqOAU6S.SX380_SY500_CR,0,0,38,50_BG85,'
                          '85,85_BR-120_PKdp-play-icon-overlay__.png') == (380, 500)

    def test_product(self):
        assert list(product([Category('', '', [Variation('a', 0), Variation('b', 1), Variation('c', 2)], True)])) \
               == [[[Variation(name='a', value=0), True]], [[Variation(name='b', value=1), True]],
                   [[Variation(name='c', value=2), True]]]
        assert list(product([Category('', '', [Variation('a', 0), Variation('b', 1), Variation('c', 2)], True),
                             Category('', '', [Variation('a', 0), Variation('b', 1)], True)])) \
               == [[[Variation(name='a', value=0), True], [Variation(name='a', value=0), True]],
                   [[Variation(name='a', value=0), True], [Variation(name='b', value=1), True]],
                   [[Variation(name='b', value=1), True], [Variation(name='a', value=0), True]],
                   [[Variation(name='b', value=1), True], [Variation(name='b', value=1), True]],
                   [[Variation(name='c', value=2), True], [Variation(name='a', value=0), True]],
                   [[Variation(name='c', value=2), True], [Variation(name='b', value=1), True]]]

    def test_parse_asin_from_url(self):
        assert parse_asin_from_url('https://www.amazon.com/Handle-with-Care/dp/B08KZMKWQW/ref=sr_1_4?'
                                   'dchild=1&keywords=Walking+Dead&qid=1625458858&sr=8-4') == 'B08KZMKWQW'
        assert parse_asin_from_url(
            'https://www.amazon.com/gp/slredirect/picassoRedirect.html/ref=pa_sp_mtf_aps_sr_pg1_1'
            '?ie=UTF8&adId=A04795201Z6TXX88LK5BR&url=%2FWalking-Autographed-Reprint-Bernthal-Chandler'
            '%2Fdp%2FB07VGZF192%2Fref%3Dsr_1_10_sspa%3Fdchild%3D1%26keywords%3DWalking%2BDead%26qid'
            '%3D1625458858%26sr%3D8-10-spons%26psc%3D1&qualifier=1625458858'
            '&id=600872970694646&widgetName=sp_mtf') == 'B07VGZF192'
        assert parse_asin_from_url(
            'https://www.amazon.co.jp/Star-Wars-Jedi%E2%84%A2-Visual-Dictionary/dp/0241281091/ref=sr_1_1'
            '?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=starwars'
            '&qid=1625444593&s=books&sr=1-1') == '0241281091'
        assert parse_asin_from_url('https://www.amazon.co.jp/this_isnt_valid') == None


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
            Scraper(country, run_init=False).init()

    def test_get_product_type(self):
        if not DoHeavyTest:
            return
        assert isinstance(self.scraper.get_product('B07RPQRPR5'), ProductVariations)
        assert isinstance(self.scraper.get_product('B08GG1QSRR'), ProductVariations)
        assert isinstance(self.scraper.get_product('B09319VMGT'), ProductVariations)
        assert isinstance(self.scraper.get_product('B084G2VWFW'), Product)
        assert isinstance(self.scraper.get_product('B097XB91KH'), Book)
        assert isinstance(self.scraper.get_product('4798121967'), Book)
        assert isinstance(self.scraper.get_product('B00GRKD6XU'), Kindle)
        assert isinstance(self.scraper.get_product('B08DG5HVJ6'), Movie)
        assert isinstance(self.scraper.get_product('B076B9NB4F'), PrimeVideoTV)
        assert isinstance(self.scraper.get_product('B07X1QB6NP'), PrimeVideoMovie)
        assert isinstance(self.scraper.get_product('B00L9MXVVI'), PrimeVideoMovie)


if __name__ == '__main__':
    pytest.main()
