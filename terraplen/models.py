import os
from datetime import date, datetime
from enum import Enum
from html import unescape
from typing import List, Dict, Union, Tuple, Optional
from warnings import warn

from terraplen.utils import thumb_size


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

    @property
    def lang_and_currency(self) -> Tuple[Language, Currency]:
        """
        default language and currency for Country
        :return: Tuple[Language, Currency]
        """
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

    @property
    def amazon_merchant_id(self) -> str:
        """
        Amazon's Merchant ID in Current Region.
        :return: str. merchantId
        """
        return {
            Country.Australia: "ANEGB3WVEVKZB",
            Country.Brazil: "A1ZZFT5FULY4LN",
            Country.Canada: "A3DWYIK6Y9EEQB",
            Country.ChinaMainland: "A1AJ19PSB66TGU",
            Country.France: "A1X6FK5RDHNB96",
            Country.Germany: "A3JWKAKR8XB7XF",
            Country.India: "AT95IG9ONZD7S",
            Country.Italy: "A11IL2PNWYJU7H",
            Country.Japan: "AN1VRQENFRJN5",
            Country.Mexico: "AVDBXBAVVSXLQ",
            Country.Netherlands: "A17D2BRD4YMT0X",
            Country.Poland: "A5JH7MGCI556L",
            Country.SaudiArabia: "A2XPWB6MYN7ZDK",
            Country.Singapore: "ACT6OAM3OSC9S",
            Country.Spain: "A1AT7YVPFBWXBL",
            Country.Sweden: "ANU9KP01APNAG",
            Country.Turkey: "A3IUCL7SEZP27A",
            Country.UnitedArabEmirates: "A2KKU8J8O8784X",
            Country.UnitedKingdom: "A3P5ROKL5A1OLE",
            Country.UnitedStates: "ATVPDKIKX0DER",
        }[self]


class Offer:
    def __init__(self, price: Union[float, None], currency: str, rating: float, condition: str, ships_from: str,
                 sold_by: str, sold_by_url: str):
        """
        offer for product
        :param price: price of offer
        :param currency: currency of offer
        :param rating: rating of seller
        :param condition: condition of product
        :param ships_from: ships from
        :param sold_by: seller name
        :param sold_by_url: seller's page
        """
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
    def __init__(self, asin: str, product_name: str, offer_count: int, offers: List[Offer], settings: Dict[str, bool],
                 is_last_page=False):
        """
        container of Offer
        :param asin: asin of product
        :param product_name: products name
        :param offer_count: total offers count
        :param offers: offers
        :param settings: settings of offers filter
        """
        self.asin = asin
        self.product_name = unescape(product_name)
        self.offer_count = offer_count
        self.offers = offers
        self.page = settings['page']
        self.settings = settings
        self.is_last_page = is_last_page

    def __repr__(self):
        return 'OfferList(asin={!r}, product_name={!r}, offer_count={}, ' \
               'offers={!r}, page={}, settings={!r}, is_last_page={})'.format(self.asin, self.product_name,
                                                                              self.offer_count, self.offers, self.page,
                                                                              self.settings, self.is_last_page)


class Review:
    def __init__(self, reviewer: str, reviewer_url: str, review_url: str, title: str, rating: int, helpful: int,
                 body: str):
        """
        class for a single review
        :param reviewer: reviewer's name
        :param reviewer_url: reviewer's page
        :param review_url: review page
        :param title: title of review
        :param rating: rating of product
        :param helpful: how many people found this review helpful
        :param body: body text
        """
        self.reviewer = unescape(reviewer)
        self.reviewer_url = reviewer_url
        self.review_url = review_url
        self.title = unescape(title)
        self.rating = rating
        self.helpful = helpful
        self.body = unescape(body)

    def __repr__(self):
        return 'Review(reviewer={!r}, reviewer_url={!r}, review_url={!r}, title={!r}, rating={}, helpful={}, body={!r})'.format(
            self.reviewer, self.reviewer_url, self.review_url,
            self.title, self.rating, self.helpful, self.body)


class ReviewList:
    def __init__(self, reviews: List[Review], asin: str, country: Country, settings: 'ReviewSettings',
                 page: int, is_last_page: bool):
        """
        review container
        :param reviews: reviews
        :param asin: asin of product
        :param country: country these reviews written in
        :param settings: settings of review filter
        :param is_last_page: whether this is the last page of reviews
        """
        self.reviews = reviews
        self.asin = asin
        self.country = country
        self.settings = settings
        self.page = page
        self.is_last_page = is_last_page

    def __repr__(self):
        return 'ReviewList(reviews={!r}, asin={!r}, country={}, ' \
               'settings={!r}, page={}, is_last_page={})'.format(self.reviews, self.asin, self.country,
                                                                 self.page, self.settings, self.is_last_page)


class ReviewParameter:
    """
    parameters for review settings
    """

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
                 filter_by_language: Union[str, Language] = '', keyword='', page_size=10):
        """
        Settings for review search
        :param sort_by: sorting setting. defaults to `ReviewParameter.SortBy.Helpful`
        :param reviewer_type: whether filter with verified purchased reviewer or not.
        defaults to `ReviewParameter.ReviewerType.AllReviews`
        :param format_type: whether filter with current format(variation) of product.
        defaults to `ReviewParameter.FormatType.AllFormats`
        :param media_type: filter of review's content type. defaults to `ReviewParameter.MediaType.AllContents`
        :param filter_by_star: filter of review's star and evaluation.
        defaults to `ReviewParameter.FilterByStar.AllStars`
        :param filter_by_language: filter of review language.
        :param keyword: if given, filter reviews with keyword.
        :param page_size: how many reviews to be in a single page. up to 20.
        """
        self.sort_by = sort_by
        self.reviewer_type = reviewer_type
        self.format_type = format_type
        self.media_type = media_type
        self.filter_by_star = filter_by_star
        if isinstance(filter_by_language, Language):
            filter_by_language = filter_by_language.value
        self.filter_by_language = filter_by_language
        self.keyword = keyword
        if not 1 <= page_size <= 20:
            warn('page_size `{}` is invalid. needs to be between 1 and 20. set to 10.'.format(page_size))
            page_size = 10
        self.page_size = page_size

    def to_dict(self, asin: str, page: int) -> Dict:
        """
        create dict to pass to amazon
        """
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

                'pageNumber': page,  # default=1
                'filterByLanguage': self.filter_by_language,
                'filterByKeyword': self.keyword,  # search
                'shouldAppend': 'undefined',
                'deviceType': 'desktop',
                'canShowIntHeader': 'undefined',
                'reftag': 'cm_cr_getr_d_paging_btm_next_{}'.format(self.page_number),
                'pageSize': self.page_size,  # default=10, max=20, min=1
                'asin': asin,
                'scope': 'reviewsAjax1'}

    def copy(self) -> 'ReviewSettings':
        return ReviewSettings(self.sort_by, self.reviewer_type, self.format_type,
                              self.media_type, self.filter_by_star, self.filter_by_language,
                              self.keyword, self.page_size)

    def __repr__(self):
        return 'ReviewSettings(sort_by={!r}, reviewer_type={!r}, format_type={!r}, ' \
               'media_type={!r}, filter_by_star={!r}, ' \
               'filter_by_language={!r}, keyword={!r}, page_size={})'.format(self.sort_by, self.reviewer_type,
                                                                             self.format_type, self.media_type,
                                                                             self.filter_by_star,
                                                                             self.filter_by_language, self.keyword,
                                                                             self.page_size)


class VideoImage:
    def __init__(self, url: str, width: int, height: int, extension: str = ''):
        """
        thumbnail for video of product
        :param url: url of image
        :param width: width of image
        :param height: height of image
        :param extension: extension of image. 'png' for instance.
        """
        self.url = url
        self.width = width
        self.height = height
        if not extension:
            extension = os.path.splitext(url)[1][1:]
        self.extension = extension

    def __repr__(self):
        return 'VideoImage(url={!r}, width={}, height={}, extension={!r})'.format(self.url, self.width, self.height,
                                                                                  self.extension)


class Video:
    def __init__(self, duration_seconds: int, duration_timestamp: str, is_hero_video: bool, language_code: str,
                 slate: VideoImage, thumb: VideoImage, title: str, url: str, variant: 'Product', width: int,
                 height: int):
        """
        video of product
        :param duration_seconds: seconds of video duration
        :param duration_timestamp: display of video duration. '01:24' for instance
        :param is_hero_video: whether this is hero video or not
        :param language_code: language code of video
        :param slate: slate image
        :param thumb: thumbnail of video
        :param title: title of video
        :param url: url of video
        :param variant: variant of product of this video
        :param width: width of video
        :param height: height of video
        """
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
        return 'Video(duration_seconds={}, duration_timestamp={!r}, is_hero_video={!r}, ' \
               'language_code={!r}, slate={!r}, thumb={!r}, title={!r}, ' \
               'url={!r}, variant={!r}, width={}, height={})'.format(self.duration_seconds, self.duration_timestamp,
                                                                     self.is_hero_video, self.language_code,
                                                                     self.slate, self.thumb, self.title, self.url,
                                                                     self.variant, self.width, self.height)


class Variation:
    def __init__(self, name: str, value: int):
        """
        variation of product's categories
        :param name: display name of variation
        :param value: value of variation
        """
        self.name = unescape(name)
        self.value = value

    def __repr__(self):
        return 'Variation(name={!r}, value={})'.format(self.name, self.value)

    def __eq__(self, other):
        return isinstance(other, Variation) and self.name == other.name and self.value == other.value


class Category:
    def __init__(self, name: str, display_name: str, variations: List[Variation], is_visual: bool):
        """
        category of product. container of variations
        :param name: name of category
        :param display_name: display_name of category. This depends on current Language
        :param variations: variations of category
        :param is_visual: whether this category is visual variation
        """
        self.name = name
        self.display_name = unescape(display_name)
        self.variations = variations
        self.is_visual = is_visual

    def __repr__(self):
        return 'Category(name={!r}, display_name={!r}, variations={!r}), is_visual={}'.format(self.name,
                                                                                              self.display_name,
                                                                                              self.variations,
                                                                                              self.is_visual)


class ProductImage:
    def __init__(self, hi_res: str, large: str, thumb: str, variant: str, main: Dict[str, Tuple[int, int]]):
        """
        Each product image
        :param hi_res: hi_res image url
        :param large: large image url
        :param thumb: thumbnail url
        :param variant: variant of this image
        :param main: other image size. dict[image_url, (height, width)]
        """
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
        """
        largest image
        """
        if self.hi_res:
            return self.hi_res
        if self.large:
            return self.large
        if self.main:
            return sorted(list(self.main.items()), key=lambda x: x[1])[-1][0]
        return self.thumb

    def __repr__(self):
        return 'ProductImage(hi_res={!r}, variant={!r}, thumb={!r}, ' \
               'variant={!r}, main={!r})'.format(self.hi_res, self.variant, self.thumb, self.variant, self.main)


class MediaImage:
    def __init__(self, main: str, thumb: str, width: int, height: int):
        """
        images for books, movies
        :param main: image url
        :param thumb: thumbnail of image
        :param width: width of image
        :param height: height of image
        """
        self.main = main
        self.thumb = thumb
        self.width = width
        self.height = height

    @classmethod
    def from_json(cls, data: Dict) -> 'MediaImage':
        return MediaImage(data['mainUrl'], data['thumbUrl'], *data['dimensions'])

    @property
    def largest_image(self) -> str:
        """
        largest image
        """
        if self.main:
            return self.main
        return self.thumb

    def __repr__(self):
        return 'MediaImage(main={!r}, thumb={!r}, width={}, height={})'.format(self.main, self.thumb, self.width,
                                                                               self.height)


class Product:
    def __init__(self, asin: str, title: str, variation: List[Variation], images: List[ProductImage],
                 videos: List[Video], hero_images: List[ProductImage], hero_videos=List[Video]):
        """
        product data
        :param asin: asin of product
        :param title: title of product
        :param variation: variation of product
        :param images: images of product
        :param videos: videos of product
        :param hero_images: hero images of product
        :param hero_videos: hero videos of product
        """
        self.asin = asin
        self.title = unescape(title)
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
        """
        variation of books and movies
        :param name: name of variation
        :param price: price of variation
        :param asin: asin of variation
        """
        self.name = unescape(name)
        self.price = price
        self.asin = asin

    def __repr__(self):
        return 'MediaVariation(name={!r}, price={!r}, asin={!r})'.format(self.name, self.price, self.asin)


class Book:
    def __init__(self, asin: str, title: str, images: List[MediaImage], videos: List[Video],
                 variations: List[MediaVariation], current_variation: MediaVariation):
        """
        book data
        :param asin: asin of book
        :param title: title of book
        :param images: images of book
        :param videos: videos of book
        :param variations: book's variations.
        :param current_variation: current variation
        """
        self.asin = asin
        self.title = unescape(title)
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
        """
        movie data
        :param asin: asin of movie
        :param title: title of movie
        :param images: images of movie
        :param videos: videos of movie
        :param variations: movie's variations.
        :param current_variation: current variation
        """
        self.asin = asin
        self.title = unescape(title)
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
        """
        Kindle book data
        :param asin: asin of Kindle
        :param title: title of Kindle
        :param image: images of Kindle
        :param variations: Kindle's variations.
        :param current_variation: current variation
        """
        self.asin = asin
        self.title = unescape(title)
        self.image = image
        self.variations = variations
        self.current_variation = current_variation

    def __repr__(self):
        return 'Kindle(asin={!r}, title={!r}, image={!r}, ' \
               'variations={!r}, current_variation={!r})'.format(self.asin, self.title, self.image,
                                                                 self.variations, self.current_variation)


class ProductVariations:
    def __init__(self, title: str, products: List[Product], landing: Product, parent_asin: str,
                 categories: List[Category]):
        """
        container for Product which has variations
        :param title: title of product
        :param products: all products with variations
        :param landing: landing product.
        :param parent_asin: parent product's asin
        :param categories: all categories
        """
        self.title = unescape(title)
        self.products = products
        self.landing = landing
        self.parent_asin = parent_asin
        self.categories = categories

    def __repr__(self):
        return 'ProductVariations(title={!r}, products={!r}, landing={!r}, ' \
               'parent_asin={!r}, categories={!r})'.format(self.title, self.products, self.landing,
                                                           self.parent_asin,
                                                           self.categories)


class PrimeVideoOption:
    def __init__(self, asin: str, is_prime: bool, purchase_type: str, price: str, video_quality: str):
        """
        prime video's purchase options
        :param asin: asin of option
        :param is_prime: whether this option is prime
        :param purchase_type: purchase type
        :param price: price
        :param video_quality: video quality
        """
        self.asin = asin
        self.is_prime = is_prime
        self.purchase_type = unescape(purchase_type)
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
        """
        prime video movie data
        :param asin: asin of prime video movie
        :param title: title of prime video movie
        :param options: options of prime video movie
        :param realm: realm of prime video movie
        :param locale: locale of prime video movie
        :param territory: territory of prime video movie
        """
        self.asin = asin
        self.title = unescape(title)
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
        """
        prime video tv series's season info
        :param asin: asin of season
        :param title: title of season
        :param rating: rating of season
        :param image_url: packshot's url
        :param is_prime: whether this season is prime
        :param maturity_rating: maturity rating
        :param release_date: release date
        :param season_number: season number
        :param synopsis: synopsis
        :param title_type: title type. 'season' for instance.
        """
        self.asin = asin
        self.title = unescape(title)
        self.rating = rating
        self.image_url = image_url
        self.is_prime = is_prime
        self.maturity_rating = maturity_rating
        self.release_date = release_date
        self.season_number = season_number
        self.synopsis = unescape(synopsis)
        self.title_type = title_type

    @classmethod
    def from_json(cls, asin: str, data: Dict) -> 'PrimeVideoTVSeason':
        _date = datetime.strptime(data['releaseDate'], '%Y/%m/%d').date()
        return PrimeVideoTVSeason(asin, data['title'], data['amazonRating']['value'], data['images']['packshot'],
                                  data['isPrime'], data['ratingBadge']['id'], _date, data['seasonNumber'],
                                  data['synopsis'], data['titleType'])

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
        """
        prime video TV data
        :param asin: asin of prime video TV
        :param title: title of prime video TV
        :param options: options of prime video TV
        :param seasons: seasons of prime video TV
        :param realm: realm of prime video TV
        :param locale: locale of prime video TV
        :param territory: territory of prime video TV
        """
        self.asin = asin
        self.title = unescape(title)
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


class SearchCategory(Enum):
    AlexaSkills = 'alexa-skills'
    AllDepartments = 'aps'
    AmazonDevices = 'amazon-devices'
    AmazonFresh = 'nowstore'
    AmazonGlobalStore = 'amazon-global-store'
    AmazonWarehouse = 'warehouse-deals'
    Apparel = 'apparel'
    AppsAndGames = 'mobile-apps'
    ArtsAndcrafts = 'arts-crafts'
    AudibleAudiobooks = 'audible'
    AudioVisual = 'audio-visual'
    Baby = 'baby'
    Beauty = 'beauty'
    Books = 'stripbooks'
    CameraAndPhoto = 'photo'
    CarAndMotorbike = 'automotive'
    CarRenting = 'vehicles'
    ClassicalMusic = 'classical'
    Clothing = 'clothing'
    Collectibles = 'collectibles'
    Communications = 'communications'
    ComputersAndAccessories = 'computers'
    DIYAndTools = 'diy'
    DVDAndBluray = 'dvd'
    DigitalMusic = 'digital-music'
    ElectronicsAndPhoto = 'electronics'
    EnglishBook = 'english-books'
    Fashion = 'fashion'
    FashionBaby = 'fashion-baby'
    FashionBabyAndKids = 'fashion-baby-kids'
    FashionBoys = 'fashion-boys'
    FashionGirls = 'fashion-girls'
    FashionMen = 'fashion-mens'
    FashionWomen = 'fashion-womens'
    Financial = 'financial'
    FoodDrinkAndAlcohol = 'food-beverage'
    Furniture = 'furniture'
    GardenAndOutdoor = 'lawngarden'
    GardenAndOutdoors = 'outdoor'
    GiftCards = 'gift-cards'
    Grocery = 'grocery'
    Handmade = 'handmade'
    HealthAndPersonalCare = 'drugstore'
    HealthHouseholdAndPersonalCare = 'hpc'
    Hobby = 'hobby'
    Home = 'home'
    HomeAndBusinessServices = 'local-services'
    HomeAndGarden = 'garden'
    HomeAndKitchen = 'kitchen'
    HomeAppliance = 'home-appliances'
    HomeImprovement = 'hi'
    HomeSubstore = 'home-substore'
    IndustrialAndScientific = 'industrial'
    Jewellery = 'jewelry'
    KindleStore = 'digital-text'
    LargeAppliances = 'appliances'
    Lighting = 'lighting'
    Luggage = 'luggage'
    LuggageAndTravelGear = 'fashion-luggage'
    Magazines = 'magazines'
    Misc = 'misc'
    MoviesAndTV = 'movies-tv'
    MusicCDsAndVinyl = 'popular'
    MusicPlayers = 'music-players'
    MusicalInstrumentsAndDJEquipment = 'mi'
    PCAndVideoGames = 'videogames'
    Pantry = 'pantry'
    PetSupplies = 'pets'
    PhotoAndVideo = 'photo-video'
    PremiumBeauty = 'luxury-beauty'
    PrimeVideo = 'instant-video'
    ShoesAndBags = 'shoes'
    SmartHome = 'smart-home'
    Software = 'software'
    SportsAndOutdoors = 'sporting'
    StationeryAndOfficeSupplies = 'office-products'
    SubscribeAndSave = 'specialty-aps-sns'
    TodaysDeals = 'todays-deals'
    ToolsAndHomeImprovement = 'tools'
    ToysAndGames = 'toys'
    UnderTenDollars = 'under-ten-dollars'
    Watches = 'watch'
    Wine = 'wine'
    WineBeerAndSpirits = 'alcohol'

    def value_by_country(self, country: Country) -> str:
        """
        some categories has different values for region. Resolve correct value for current region.
        """
        if self is SearchCategory.HomeImprovement:
            if country in (Country.Sweden, Country.Singapore, Country.SaudiArabia, Country.Poland, Country.Netherlands,
                           Country.India, Country.ChinaMainland, Country.Australia):
                return 'home-improvement'
        elif self is SearchCategory.SportsAndOutdoors:
            if country in (Country.UnitedKingdom, Country.UnitedArabEmirates, Country.Turkey, Country.SaudiArabia,
                           Country.Netherlands, Country.Germany, Country.France):
                return 'sports'
        elif self is SearchCategory.ToysAndGames:
            if country in (Country.UnitedStates, Country.ChinaMainland):
                return 'toys-and-games'
        return str(self)


class SearchResultProductOffers:
    def __init__(self, asin: str, offer_name: str, currency: str, price: float):
        """
        offer of search result product
        :param asin: asin of offer
        :param offer_name: offer_name of offer
        :param currency: currency of offer
        :param price: price of offer
        """
        self.asin = asin
        self.offer_name = unescape(offer_name)
        self.currency = currency
        self.price = price

    def __repr__(self):
        return 'SearchResultProductOffers(asin={!r}, offer_name={!r}, ' \
               'currency={!r}, price={!r})'.format(self.asin, self.offer_name, self.currency, self.price)


class SearchResultProduct:
    def __init__(self, asin: str, name: str, currency: str, min_price: float, offers: List[SearchResultProductOffers]):
        """
        each product of search result
        :param asin: asin of product
        :param name: name of product
        :param currency: currency of product
        :param min_price: min price of offers
        :param offers: offers for product
        """
        self.asin = asin
        self.name = unescape(name)
        self.currency = currency
        self.min_price = min_price
        self.offers = offers

    def __repr__(self):
        return 'SearchResultProduct(asin={!r}, name={!r}, ' \
               'currency={!r}, min_price={!r}, offers={!r})'.format(self.asin, self.name, self.currency,
                                                                    self.min_price, self.offers)


class SearchResult:
    def __init__(self, result: List[SearchResultProduct], keyword: str, page: int, min_price: int, max_price: int,
                 merchant: str, category: SearchCategory, last_page: Optional[int], is_last_page: bool):
        """
        result of search
        :param result: result of search
        :param keyword: keyword of search
        :param page: page number of result
        :param min_price: min price of search filtering
        :param max_price: max price of search filtering
        :param merchant: merchant id of search filtering
        :param category: category filtering
        :param last_page: last page number. if current page exceeds last_page, terraplen cant parse last_page from html.
        so, last_page will be None.
        :param is_last_page: whether this is last page
        """
        self.result = result
        self.keyword = keyword
        self.page = page
        self.min_price = min_price
        self.max_price = max_price
        self.merchant = merchant
        self.category = category
        self.last_page = last_page
        self.is_last_page = is_last_page

    def __repr__(self):
        return 'SearchResult(result={!r}, keyword={!r}, page={}, min_price={}, max_price={}, ' \
               'merchant={!r}, category={!r}, last_page={}, is_last_page={})'.format(self.result, self.keyword,
                                                                                     self.page,
                                                                                     self.min_price, self.max_price,
                                                                                     self.merchant,
                                                                                     self.category, self.last_page,
                                                                                     self.is_last_page)
