from enum import Enum
from warnings import warn
from typing import List, Dict, Union, Tuple
import os
from terraplen.utils import thumb_size
from datetime import date, datetime


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
        return ('Offer(price={}, currency={!r}, approx_review={}, condition={!r}, '
                'ships_from={!r}, sold_by={!r}, sold_by_url={!r})').format(self.price, self.currency,
                                                                           self.approx_review, self.condition,
                                                                           self.ships_from, self.sold_by,
                                                                           self.sold_by_url)


class OfferList:
    def __init__(self, product_name: str, offer_count: int, offers: List[Offer], settings: Dict[str, bool]):
        self.product_name = product_name
        self.offer_count = offer_count
        self.offers = offers
        self.page = settings['page']
        self.settings = settings

    def __repr__(self):
        return 'OfferList(product_name={!r}, offer_count={}, ' \
               'offers={!r}, page={}, settings={!r})'.format(self.product_name, self.offer_count,
                                                             self.offers, self.page, self.settings)


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
        return 'Review(reviewer={!r}, reviewer_url={!r}, review_url={!r}, title={!r}, rating={}, helpful={}, body={!r})'.format(
            self.reviewer, self.reviewer_url, self.review_url,
            self.title, self.rating, self.helpful, self.body)


class ReviewList:
    def __init__(self, reviews: List[Review], asin: str, country: Country, settings: 'ReviewSettings', last_page=False):
        self.reviews = reviews
        self.asin = asin
        self.country = country
        self.settings = settings
        self.page = settings.page_number
        self.last_page = last_page

    def __repr__(self):
        return 'ReviewList(reviews={!r}, asin={!r}, country={}, page={}, last_page={})'.format(self.reviews,
                                                                                               self.asin,
                                                                                               self.country,
                                                                                               self.page,
                                                                                               self.last_page)


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
                 page_number: int = 1, filter_by_language: str = '', keyword='', page_size=10):
        self.sort_by = sort_by
        self.reviewer_type = reviewer_type
        self.format_type = format_type
        self.media_type = media_type
        self.filter_by_star = filter_by_star
        self.page_number = page_number
        self.filter_by_language = filter_by_language
        self.keyword = keyword
        if not 1 <= page_size <= 20:
            warn('page_size `{}` is invalid. needs to be between 1 and 20. set to 10.'.format(page_size))
            page_size = 10
        self.page_size = page_size

    def to_dict(self, asin: str) -> Dict:
        return {'sortBy': self.sort_by.value,
                # 'recent' or 'helpful'(default)

                'reviewerType': self.reviewer_type.value,
                # 'avp_only_reviews' (Verified purchase) or
                # 'all_reviews'(default)

                'formatType': self.format_type.value,
                # 'current_format' or 'all_formats'(default)

                'mediaType': self.media_type.value,
                # 'media_reviews_only' or 'all_contents'(default)

                'filterByStar': self.filter_by_star.value,
                # {'one', 'two', 'three', 'four', 'five'} + '_star' or
                # 'positive' or 'critical' or 'all_stars'(default)

                'pageNumber': self.page_number,  # default=1
                'filterByLanguage': self.filter_by_language,
                'filterByKeyword': self.keyword,  # search
                'shouldAppend': 'undefined',
                'deviceType': 'desktop',
                'canShowIntHeader': 'undefined',
                'reftag': 'cm_cr_getr_d_paging_btm_next_{}'.format(self.page_number),
                'pageSize': self.page_size,  # default=10, max=20, min=1
                'asin': asin,
                'scope': 'reviewsAjax1'}


class VideoImage:
    def __init__(self, url: str, width: int, height: int, extension: str = ''):
        self.url = url
        self.width = width
        self.height = height
        if not extension:
            extension = os.path.splitext(url)[1][1:]
        self.extension = extension


class Video:
    def __init__(self, duration_seconds: int, duration_timestamp: str, is_hero_video: bool, language_code: str,
                 slate: VideoImage, thumb: VideoImage, title: str, url: str, variant: 'Product', width: int,
                 height: int):
        self.duration_seconds = duration_seconds
        self.duration_timestamp = duration_timestamp
        self.is_hero_video = is_hero_video
        self.language_code = language_code
        self.slate = slate
        self.thumb = thumb
        self.title = title
        self.url = url
        self.variant = variant
        self.width = width
        self.height = height

    @classmethod
    def from_json(cls, data: Dict) -> 'Video':
        if not data['isVideo']:
            raise TypeError("This is not a video.")
        slate = VideoImage(data['slateUrl'], data['slateHash']['width'],
                           data['slateHash']['height'], data['slateHash']['extension'])
        thumb = VideoImage(data['thumbUrl'], *thumb_size(data['thumbUrl']))
        return Video(duration_seconds=data['durationSeconds'], duration_timestamp=data['durationTimestamp'],
                     is_hero_video=data['isHeroVideo'], language_code=data['languageCode'], slate=slate,
                     thumb=thumb, title=data['title'], url=data['url'], variant=data['variant'],
                     width=data['videoWidth'], height=data['videoHeight'])

    def __repr__(self):
        return 'Video(duration_seconds={}, ' \
               'language_code={!r}, title={!r}, url={!r})'.format(self.duration_seconds, self.language_code,
                                                                  self.title, self.url)


class Variation:
    def __init__(self, name: str, value: int):
        self.name = name
        self.value = value

    def __repr__(self):
        return 'Variation(name={!r}, value={})'.format(self.name, self.value)

    def __eq__(self, other):
        return isinstance(other, Variation) and self.name == other.name and self.value == other.value


class Category:
    def __init__(self, name: str, display_name: str, variations: List[Variation]):
        self.name = name
        self.display_name = display_name
        self.variations = variations

    def __repr__(self):
        return 'Category(name={!r}, display_name={!r}, variations={!r})'.format(self.name,
                                                                                self.display_name,
                                                                                self.variations)


class ProductImage:
    def __init__(self, hi_res: str, large: str, thumb: str, variant: str, main: Dict[str, Tuple[int, int]]):
        self.hi_res = hi_res
        self.large = large
        self.thumb = thumb
        self.variant = variant
        self.main = main

    @classmethod
    def from_json(cls, data: Dict) -> 'ProductImage':
        return ProductImage(data.get('hiRes'), data.get('large'), data.get('thumb'), data.get('variant'),
                            {k: tuple(v) for k, v in data.get('main', {}).items()})

    @property
    def largest_image(self) -> str:
        if self.hi_res:
            return self.hi_res
        if self.large:
            return self.large
        if self.main:
            return sorted([self.main.items()], key=lambda x: x[1])[-1][0]

    def __repr__(self):
        return 'ProductImage(hi_res={!r}, variant={!r})'.format(self.hi_res, self.variant)


class MediaImage:
    def __init__(self, main: str, thumb: str, width: int, height: int):
        self.main = main
        self.thumb = thumb
        self.width = width
        self.height = height

    @classmethod
    def from_json(cls, data: Dict) -> 'MediaImage':
        return MediaImage(data['mainUrl'], data['thumbUrl'], *data['dimensions'])

    @property
    def largest_image(self) -> str:
        if self.main:
            return self.main
        return self.thumb

    def __repr__(self):
        return 'MediaImage(main={}, thumb={}, width={}, height={})'.format(self.main, self.thumb, self.width,
                                                                           self.height)


class Product:
    def __init__(self, asin: str, title: str, variation: List[Variation], images: List[ProductImage],
                 videos: List[Video], hero_images: List[ProductImage], hero_videos=List[Video]):
        self.asin = asin
        self.title = title
        self.variation = variation
        self.images = images
        self.videos = videos
        self.hero_images = hero_images
        self.hero_videos = hero_videos

    def __repr__(self):
        return 'Product(asin={!r}, title={!r}, variation={!r}, images={!r}, ' \
               'videos={!r}, hero_images={!r}, hero_videos={!r})'.format(self.asin, self.title,
                                                                         self.variation, self.images,
                                                                         self.videos, self.hero_images,
                                                                         self.hero_videos)


class MediaVariation:
    def __init__(self, name: str, price: str, asin: str):
        self.name = name
        self.price = price
        self.asin = asin

    def __repr__(self):
        return 'MediaVariation(name={!r}, price={!r}, asin={!r})'.format(self.name, self.price, self.asin)


class Book:
    def __init__(self, asin: str, title: str, images: List[MediaImage], videos: List[Video],
                 variations: List[MediaVariation], current_variation: MediaVariation):
        self.asin = asin
        self.title = title
        self.images = images
        self.videos = videos
        self.variations = variations
        self.current_variation = current_variation

    def __repr__(self):
        return 'Book(asin={!r}, title={!r}, images={!r}, videos={!r}, ' \
               'variations={!r}, current_variation={!r})'.format(self.asin, self.title,
                                                                 self.images, self.videos,
                                                                 self.variations, self.current_variation)


class Movie:
    def __init__(self, asin: str, title: str, images: List[ProductImage], videos: List[Video],
                 variations: List[MediaVariation], current_variation: MediaVariation):
        self.asin = asin
        self.title = title
        self.images = images
        self.videos = videos
        self.variations = variations
        self.current_variation = current_variation

    def __repr__(self):
        return 'Movie(asin={!r}, title={!r}, images={!r}, videos={!r}, ' \
               'variations={!r}, current_variation={!r})'.format(self.asin, self.title,
                                                                 self.images, self.videos,
                                                                 self.variations, self.current_variation)


class Kindle:
    def __init__(self, asin: str, title: str, image: MediaImage,
                 variations: List[MediaVariation], current_variation: MediaVariation):
        self.asin = asin
        self.title = title
        self.image = image
        self.variations = variations
        self.current_variation = current_variation

    def __repr__(self):
        return 'Kindle(asin={!r}, title={!r}, image={!r}, ' \
               'variations={!r}, current_variation={!r})'.format(self.asin, self.title, self.image,
                                                                 self.variations, self.current_variation)


class ProductVariations:
    def __init__(self, products: List[Product], landing: Product, parent_asin: str, title: str,
                 categories: List[Category]):
        self.products = products
        self.landing = landing
        self.parent_asin = parent_asin
        self.title = title
        self.categories = categories

    def __repr__(self):
        return 'ProductVariations(products={!r}, landing={!r}, ' \
               'parent_asin={!r}, title={!r}, categories={!r})'.format(self.products, self.landing,
                                                                       self.parent_asin, self.title,
                                                                       self.categories)


class PrimeVideoOption:
    def __init__(self, asin: str, is_prime: bool, purchase_type: str, price: str, video_quality: str):
        self.asin = asin
        self.is_prime = is_prime
        self.purchase_type = purchase_type
        self.price = price
        self.video_quality = video_quality

    def __repr__(self):
        return 'PrimeVideoOption(asin={!r}, is_prime={}, ' \
               'purchase_type={!r}, price={!r}, video_quality={!r})'.format(self.asin, self.is_prime,
                                                                            self.purchase_type,
                                                                            self.price,
                                                                            self.video_quality)


class PrimeVideoMovie:
    def __init__(self, asin: str, title: str, options: List[PrimeVideoOption], realm: str, locale: str, territory: str):
        self.asin = asin
        self.title = title
        self.options = options
        self.realm = realm
        self.locale = locale
        self.territory = territory

    def __repr__(self):
        return 'PrimeVideoMovie(asin={!r}, title={!r}, options={!r}, ' \
               'realm={!r}, locale={!r}, territory={!r})'.format(self.asin, self.title, self.options,
                                                                 self.realm, self.locale, self.territory)


class PrimeVideoTVSeason:
    def __init__(self, asin: str, title: str, rating: int, image_url: str, is_prime: bool, maturity_rating: str,
                 release_date: date, season_number: int, synopsis: str, title_type: str):
        self.asin = asin
        self.title = title
        self.rating = rating
        self.image_url = image_url
        self.is_prime = is_prime
        self.maturity_rating = maturity_rating
        self.release_date = release_date
        self.season_number = season_number
        self.synopsis = synopsis
        self.title_type = title_type

    @classmethod
    def from_json(cls, asin: str, data: Dict) -> 'PrimeVideoTVSeason':
        _date = datetime.strptime(data['releaseDate'], '%Y/%m/%d').date()
        return PrimeVideoTVSeason(asin, data['title'], data['amazonRating']['value'], data['images']['packshot'],
                                  data['isPrime'], data['ratingBadge']['id'], _date, data['seasonNumber'],
                                  data['title'], data['titleType'])

    def __repr__(self):
        return 'PrimeVideoTVSeason(asin={!r}, title={!r}, rating={}, ' \
               'image_url={!r}, is_prime={}, maturity_rating={!r}, ' \
               'release_date={!r}, season_number={}, synopsis={!r}, ' \
               'title_type={!r})'.format(self.asin, self.title, self.rating, self.image_url, self.is_prime,
                                         self.maturity_rating, self.release_date, self.season_number, self.synopsis,
                                         self.title_type)


class PrimeVideoTV:
    def __init__(self, asin: str, title: str, options: List[PrimeVideoOption], seasons: List[PrimeVideoTVSeason],
                 realm: str, locale: str, territory: str):
        self.asin = asin
        self.title = title
        self.options = options
        self.seasons = seasons
        self.realm = realm
        self.locale = locale
        self.territory = territory

    def __repr__(self):
        return 'PrimeVideoTV(asin={!r}, title={!r}, options={!r}, ' \
               'seasons={!r}, realm={!r}, locale={!r}, territory={!r})'.format(self.asin, self.title, self.options,
                                                                               self.seasons, self.realm, self.locale,
                                                                               self.territory)


class SearchOptions:
    def __init__(self, min_price: int = None, max_price: int = None, merchant: str = None):
        self.min_price = min_price
        self.max_price = max_price
        self.merchant = merchant

    def to_value(self):
        result = []
        if self.min_price:
            result.append('low-price={}'.format(self.min_price))
        if self.max_price:
            result.append('high-price={}'.format(self.max_price))
        if self.merchant:
            result.append('emi={}'.format(self.merchant))


class SearchResult:
    pass
