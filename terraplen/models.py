from enum import Enum
from typing import List, Dict, Union, Tuple


class UserAgents:
    def __init__(self, head: str, version: List[str]):
        self.head = head
        self.version = version

        self.index = -1

    def get_next_user_agent(self):
        self.index = (self.index + 1) % len(self.version)
        return '{head} {version}'.format(head=self.head, version=self.version[self.index])


class Language(Enum):
    English = 'en_US'
    Spanish = 'es_ES'
    SimplifiedChinese = 'zh_CN'
    TraditionalChinese_ = 'zh_TW'
    German = 'de_DE'
    Portuguese = 'pt_BR'
    Korean = 'ko_KR'
    Hebrew = 'he_IL'
    Arabic = 'ar_AE'
    Hindi = 'hi_IN'
    Tamil = 'ta_IN'
    Telugu = 'te_IN'
    Kannada = 'kn_IN'
    Malayalam = 'ml_IN'
    Italian = 'it_IT'
    Swedish = 'sv_SE'
    French = 'fr_FR'
    Japanese = 'ja_JP'
    Dutch = 'nl_NL'
    Polish = 'pl_PL'
    Turkish = 'tr_TR'

    EnglishAustralia = 'en_AU'
    EnglishCanada = 'en_CA'
    EnglishSingapore = 'en_SG'
    EnglishSpain = 'en_ES'
    EnglishUnitedArabEmirates = 'en_AE'
    EnglishUnitedKingdom = 'en_GB'
    SpanishMexico = 'es_MX'
    SpanishUnitedStates = 'es_US'


class Currency(Enum):
    ArabEmiratesDirham = "AED"
    ArgentinePeso = "ARS"
    AustralianDollar = "AUD"
    AzerbaijanNewManat = "AZN"
    BahamasDollar = "BSD"
    BarbadianDollar = "BBD"
    BermudaDollar = "BMD"
    BrazilianReal = "BRL"
    BruneianDollar = "BND"
    BulgariaLev = "BGN"
    CanadianDollar = "CAD"
    CaymanianDollar = "KYD"
    ChileanPeso = "CLP"
    ChineseYuanRenminbi = "CNY"
    ColombianPeso = "COP"
    CostaRicanColon = "CRC"
    CzechKoruna = "CZK"
    DanishKrone = "DKK"
    DominicanRepublicPeso = "DOP"
    EgyptianPound = "EGP"
    Euro = "EUR"
    GhanaianCedi = "GHS"
    GuatemalanQuetzal = "GTQ"
    HongKongDollar = "HKD"
    HungarianForint = "HUF"
    IndianRupee = "INR"
    IndonesianRupiah = "IDR"
    IsraeliShekel = "ILS"
    JamaicanDollar = "JMD"
    JapaneseYen = "JPY"
    KazakhstanTenge = "KZT"
    KenyanShilling = "KES"
    LebanesePound = "LBP"
    MalaysianRinggit = "MYR"
    MauritianRupee = "MUR"
    MexicoPeso = "MXN"
    MoroccanDirham = "MAD"
    NamibiaDollar = "NAD"
    NewZealandDollar = "NZD"
    NigerianNaira = "NGN"
    NorwegianKrone = "NOK"
    PakistaniRupee = "PKR"
    PanamanianBalboa = "PAB"
    PeruvianSol = "PEN"
    PhilippinePeso = "PHP"
    PolishZloty = "PLN"
    Pounds = "GBP"
    QatariRiyal = "QAR"
    RomanianLei = "RON"
    RussianRuble = "RUB"
    SaudiArabianRiyal = "SAR"
    SingaporeDollar = "SGD"
    SouthKoreanWon = "KRW"
    SriLankanRupee = "LKR"
    SwedishKrona = "SEK"
    SwissFranc = "CHF"
    TaiwanNewDollar = "TWD"
    TanzaniaShilling = "TZS"
    ThaiBaht = "THB"
    TrinidadianDollar = "TTD"
    TurkishLira = "TRY"
    USDollar = "USD"


class Country(Enum):
    Australia = "com.au"
    Brazil = "com.br"
    Canada = "ca"
    ChinaMainland = "cn"
    France = "fr"
    Germany = "de"
    India = "in"
    Italy = "it"
    Japan = "co.jp"
    Mexico = "com.mx"
    Netherlands = "nl"
    Poland = "pl"
    SaudiArabia = "sa"
    Singapore = "sg"
    Spain = "es"
    Sweden = "se"
    Turkey = "com.tr"
    UnitedArabEmirates = "ae"
    UnitedKingdom = "co.uk"
    UnitedStates = "com"

    def lang_and_currency(self) -> Tuple[Language, Currency]:
        return {
            Country.Australia: (Language.EnglishAustralia, Currency.AustralianDollar),
            Country.Brazil: (Language.Portuguese, Currency.BrazilianReal),
            Country.Canada: (Language.EnglishCanada, Currency.CanadianDollar),
            Country.ChinaMainland: (Language.SimplifiedChinese, Currency.ChineseYuanRenminbi),
            Country.France: (Language.French, Currency.Euro),
            Country.Germany: (Language.German, Currency.Euro),
            Country.India: (Language.Hindi, Currency.IndianRupee),
            Country.Italy: (Language.Italian, Currency.Euro),
            Country.Japan: (Language.Japanese, Currency.JapaneseYen),
            Country.Mexico: (Language.SpanishMexico, Currency.MexicoPeso),
            Country.Netherlands: (Language.Dutch, Currency.Euro),
            Country.Poland: (Language.Polish, Currency.PolishZloty),
            Country.SaudiArabia: (Language.Arabic, Currency.SaudiArabianRiyal),
            Country.Singapore: (Language.EnglishSingapore, Currency.SingaporeDollar),
            Country.Spain: (Language.Spanish, Currency.Euro),
            Country.Sweden: (Language.Swedish, Currency.SwedishKrona),
            Country.Turkey: (Language.Turkish, Currency.TurkishLira),
            Country.UnitedArabEmirates: (Language.EnglishUnitedArabEmirates, Currency.ArabEmiratesDirham),
            Country.UnitedKingdom: (Language.EnglishUnitedKingdom, Currency.Pounds),
            Country.UnitedStates: (Language.English, Currency.USDollar)
        }[self]


class Offer:
    def __init__(self, price: Union[float, None], currency: str, rating: float, condition: str, ships_from: str,
                 sold_by: str, sold_by_url: str):
        self.price = price
        self.currency = currency
        self.approx_review = rating
        self.condition = condition
        self.ships_from = ships_from
        self.sold_by = sold_by
        self.sold_by_url = sold_by_url

    def __repr__(self):
        return ('Offer(price={}, currency={}, approx_review={}, condition={}, '
                'ships_from={}, sold_by={}, sold_by_url={})').format(self.price, repr(self.currency),
                                                                     self.approx_review, repr(self.condition),
                                                                     repr(self.ships_from), repr(self.sold_by),
                                                                     repr(self.sold_by_url))


class OfferList:
    def __init__(self, product_name: str, offer_count: int, offers: List[Offer], settings: Dict[str, bool]):
        self.product_name = product_name
        self.offer_count = offer_count
        self.offers = offers
        self.page = settings['page']
        self.settings = settings

    def __repr__(self):
        offers_repr_length = 100
        offers_repr = repr(self.offers)
        print_offers = offers_repr[:offers_repr_length]
        if offers_repr[offers_repr_length:]:
            print_offers += '...'
        return 'OfferList(product_name={}, offer_count={}, ' \
               'offers={}, page={}, settings={})'.format(repr(self.product_name), self.offer_count,
                                                         print_offers, self.page, repr(self.settings)[:30] + '...')


class Review:
    def __init__(self, reviewer: str, reviewer_url: str, review_url: str, title: str, rating: int, helpful: int,
                 body: str):
        self.reviewer = reviewer
        self.reviewer_url = reviewer_url
        self.review_url = review_url
        self.title = title
        self.rating = rating
        self.helpful = helpful
        self.body = body

    def __repr__(self):
        body_repr_length = 100
        body_repr = repr(self.body)
        print_body = body_repr[:body_repr_length]
        if body_repr[body_repr_length:]:
            print_body += '...'
        return 'Review(reviewer={}, reviewer_url={}, review_url={}, title={}, rating={}, helpful={}, body={})'.format(
            repr(self.reviewer), repr(self.reviewer_url), repr(self.review_url),
            repr(self.title), self.rating, self.helpful, print_body)


class ReviewList:
    def __init__(self, reviews: List[Review], asin: str, country: Country, settings: Dict, last_page=False):
        self.reviews = reviews
        self.asin = asin
        self.country = country
        self.settings = settings
        self.page = settings['pageNumber']
        self.last_page = last_page

    def __repr__(self):
        reviews_repr_length = 100
        reviews_repr = repr(self.reviews)
        print_reviews = reviews_repr[:reviews_repr_length]
        if reviews_repr[reviews_repr_length:]:
            print_reviews += '...'
        return 'ReviewList(reviews={}, asin={}, country={}, page={}, last_page={})'.format(print_reviews,
                                                                                           repr(self.asin),
                                                                                           self.country,
                                                                                           self.page, self.last_page)


class ReviewParameter:
    class SortBy(Enum):
        Helpful = 'helpful'
        """Sort by helpful. default"""

        Recent = 'recent'
        """Sort by recent"""

    class ReviewerType(Enum):
        AllReviews = 'all_reviews'
        """Show all reviews. default"""

        AVPOnlyReviews = 'avp_only_reviews'
        """Show only verified purchase reviews"""

    class FormatType(Enum):
        AllFormats = 'all_formats'
        """Show reviews for all format. default"""

        CurrentFormat = 'current_format'
        """Show reviews for only current format"""

    class MediaType(Enum):
        AllContents = 'all_contents'
        """Show reviews with text, image or video. default"""

        MediaReviewsOnly = 'media_reviews_only'
        """Show reviews with image or video"""

    class FilterByStar(Enum):
        AllStars = 'all_stars'
        """Show all reviews. default"""

        FiveStar = 'five_star'
        """Show reviews with 5 star"""

        FourStar = 'four_star'
        """Show reviews with 4 star"""

        ThreeStar = 'three_star'
        """Show reviews with 3 star"""

        TwoStar = 'two_star'
        """Show reviews with 2 star"""

        OneStar = 'one_star'
        """Show reviews with 1 star"""

        Positive = 'positive'
        """Show positive reviews. Maybe 5 and 4 stars."""

        Critical = 'critical'
        """Show critical reviews. Maybe 3, 2 and 1 stars."""


class ReviewSettings:
    def __init__(self,
                 sort_by: ReviewParameter.SortBy = ReviewParameter.SortBy.Helpful,
                 reviewer_type: ReviewParameter.SortBy = ReviewParameter.ReviewerType.AllReviews,
                 format_type: ReviewParameter.FormatType = ReviewParameter.FormatType.AllFormats,
                 media_type: ReviewParameter.MediaType = ReviewParameter.MediaType.AllContents,
                 filter_by_star: ReviewParameter.FilterByStar = ReviewParameter.FilterByStar.AllStars,
                 page_number: int = 1, filter_by_language: str = ''):
        pass
