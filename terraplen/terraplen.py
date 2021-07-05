import requests

from terraplen import selector
from terraplen.wrappers import retry
from terraplen.exception import (DetectedAsBotException, BotDetectedStatusCode,
                                 ProductNotFoundCode, ProductNotFoundException)
from terraplen.utils import find_number, remove_whitespace, to_json, product, parse_asin_from_url
from terraplen.models import (Offer, OfferList, Review, ReviewList, Country, UserAgents, Currency, Language,
                              ReviewSettings, ProductImage, Product, Video, MediaImage, Book, Kindle, MediaVariation,
                              Variation, ProductVariations, Category, Movie, PrimeVideoOption, PrimeVideoTVSeason,
                              PrimeVideoMovie, PrimeVideoTV, SearchCategory, SearchResultProduct,
                              SearchResultProductOffers, SearchResult)

from bs4 import BeautifulSoup
import json
from urllib.parse import quote, urljoin
from typing import Dict, Optional, List, Tuple
import re

from warnings import warn

import html


class Scraper:
    user_agents = UserAgents('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
                             ['Chrome/91.0.4472.106 Safari/537.36', 'Chrome/91.0.4472.77 Safari/537.36',
                              'Chrome/91.0.4472.114 Safari/537.36', 'Chrome/91.0.4472.101 Safari/537.36',
                              'Chrome/91.0.4472.124 Safari/537.36'])

    def __init__(self, country: Optional[Country] = Country.UnitedStates, language: Optional[Language] = None,
                 currency: Optional[Currency] = None, run_init=True):
        """
        Create Scraper Instance
        :param country: Instance of `terraplen.Country` or `str`. Language and currency will automatically be calculated if not provided. Defaults to `Country.UnitedStates.`
        :param language: Instance of `terraplen.Language` or `str`
        :param currency: Instance of `terraplen.Currency` or `str`
        :param run_init: Whether run first setup. setup accesses to Amazon homepage.
        """
        self.headers = {'User-Agent': self.user_agents.get_next_user_agent()}
        self.cookie = {}

        if not country:
            country = Country.UnitedStates
        if not language:
            language = country.lang_and_currency[0]
        if not currency:
            currency = country.lang_and_currency[1]

        self.country = country
        self.language = language
        self.currency = currency
        self.domain = ''

        self.set_country(country)
        self.set_language(language)
        self.set_currency(currency)

        self.init_have_run = False

        if run_init:
            self.init()

    def init(self):
        self.get_with_update_cookie(self._url_top_page())

    def get_with_update_cookie(self, url: str) -> requests.Response:
        resp = requests.get(url, headers=self._create_header())
        if resp.status_code == DetectedAsBotException:
            raise BotDetectedStatusCode
        if resp.status_code == ProductNotFoundCode:
            raise ProductNotFoundException
        if self.language.value != resp.cookies.get(self._language_cookie_key, self.language.value):
            warn('looks like language `{}` is not acceptable for `{}`. '
                 'Server returned to set `{}`. Language updated'.format(self.language.value, self.domain,
                                                                        resp.cookies[self._language_cookie_key]))
            self.language = Language(resp.cookies[self._language_cookie_key])
            self.set_language(resp.cookies[self._language_cookie_key])
        if self.currency.value != resp.cookies.get('i18n-prefs', self.currency.value):
            warn('looks like currency `{}` is not acceptable for `{}`. '
                 'Server returned to set `{}`'.format(self.currency.value, self.domain,
                                                      resp.cookies['i18n-prefs']))
            self.set_currency(resp.cookies['i18n-prefs'])
        self.cookie.update(resp.cookies)
        return resp

    def post_with_update_cookie(self, url: str, data: Dict) -> requests.Response:
        resp = requests.post(url, data=data, headers=self._create_header())
        if resp.status_code == DetectedAsBotException:
            raise BotDetectedStatusCode
        if resp.status_code == ProductNotFoundCode:
            raise ProductNotFoundException
        if self.language.value != resp.cookies.get(self._language_cookie_key, self.language.value):
            warn('looks like language `{}` is not acceptable for `{}`. '
                 'Server returned to set `{}`. Language updated'.format(self.language.value, self.domain,
                                                                        resp.cookies[self._language_cookie_key]))
            self.set_language(resp.cookies[self._language_cookie_key])
        if self.currency.value != resp.cookies.get('i18n-prefs', self.currency.value):
            warn('looks like currency `{}` is not acceptable for `{}`. '
                 'Server returned to set `{}`'.format(self.currency.value, self.domain,
                                                      resp.cookies['i18n-prefs']))
            self.set_currency(resp.cookies['i18n-prefs'])
        self.cookie.update(resp.cookies)
        return resp

    def set_country(self, country: Country):
        if isinstance(country, Country):
            self.country = country
        elif isinstance(country, str):
            self.country = Country(country)  # This will raise `ValueError` if `country` is invalid.

        self.domain = 'www.amazon.{}'.format(self.country.value)

    def set_currency(self, currency: Currency):
        if isinstance(currency, str):
            currency = Currency(currency)  # This will raise `ValueError` if `currency` is invalid.
        self.currency = currency
        self.cookie['i18n-prefs'] = currency.value

    def set_language(self, language: Language):
        if isinstance(language, str):
            language = Language(language)  # This will raise `ValueError` if `language` is invalid.
        self.language = language
        self.cookie[self._language_cookie_key] = self.language.value

    @property
    def _language_cookie_key(self) -> str:
        if self.country == Country.UnitedStates:
            return 'lc-main'
        else:
            return 'lc-acb{}'.format(self.country.value.split('.')[-1])

    @retry
    def get_product(self, asin: str):
        resp = self.get_with_update_cookie(self._url_product(asin))
        soup = BeautifulSoup(resp.text, 'lxml')
        image = soup.select_one('#imageBlockVariations_feature_div > script')
        if image:
            image = re.search(r"var obj = jQuery\.parseJSON\('([^']+)'\);", image.string).groups(1)[0]
            if soup.select('#twisterContainer'):  # has options
                twister = soup.select_one('#twisterJsInitializer_feature_div > script')
                twister = re.search(r"var dataToReturn = ([^;]+)", twister.string).groups(1)[0]
                twister = re.sub(r'"updateDivLists"\s*:\s*{([^}[]+\[[^]]*\],?\s*)+},', '',
                                 twister, 1)  # this is much faster
                image, twister = to_json(image), to_json(twister)

                categories: List[Category] = []
                dimensions_text = image['visualDimensions']
                title = html.unescape(image['title'])
                for index, dimension in enumerate(dimensions_text):
                    current_variation = []
                    category_display_name = twister['dimensionsDisplay'][index]
                    category = Category(dimension, category_display_name, [])

                    for value, name in enumerate(twister['variationValues'][dimension]):
                        variation = Variation(name, value)
                        current_variation.append(variation)
                    category.variations = current_variation

                    categories.append(category)
                videos = [Video.from_json(data) for data in image['videos']]
                parent_asin = image['parentAsin']
                landing = None
                products = []
                for variations, text in product(categories):
                    images = [ProductImage.from_json(data) for data in image['colorImages'][text]]
                    hero_image = image['heroImages'][text] and ProductImage.from_json(image['heroImages'][text])
                    asin = image['colorToAsin'][text]['asin']

                    current_product = Product(asin, '', variations, images, videos, hero_image)
                    products.append(current_product)

                    if text == image['landingAsinColor']:
                        landing = current_product

                return ProductVariations(products, landing, parent_asin, title, categories)


            elif soup.select('#tmmSwatches'):  # maybe book ...?
                twister = soup.select_one('#booksImageBlock_feature_div > script:nth-child(2)')
                if twister:  # book? complete
                    twister = re.findall(r'''^["']imageGalleryData["'].+$''', twister.string, re.MULTILINE)[0]
                    twister = '{' + twister + '}'
                    image, twister = to_json(image), to_json(twister)

                    variations, variation = self._get_media_variations(soup, asin)

                    title = html.unescape(image['title'])
                    images = [MediaImage.from_json(data) for data in twister['imageGalleryData']]
                    videos = [Video.from_json(data) for data in image['videos']]
                    return Book(asin=asin, title=title, images=images, videos=videos, variations=variations,
                                current_variation=variation)
                else:  # movie? complete
                    twister = re.search(r"var data = ({.+});",
                                        soup.select_one('#imageBlock_feature_div > script:nth-child(3)').string,
                                        re.DOTALL).groups(1)[0]
                    twister = '\n'.join(
                        re.findall(r'''^["'](?:colorImages|colorToAsin|heroImage|heroVideo)["'].+$''', twister,
                                   re.MULTILINE))
                    twister = '{' + twister + '}'
                    image, twister = to_json(image), to_json(twister)

                    variations, variation = self._get_media_variations(soup, asin)

                    title = html.unescape(image['title'])
                    images = [ProductImage.from_json(data) for data in twister['colorImages']['initial']]
                    videos = [Video.from_json(data) for data in image['videos']]
                    return Movie(asin=asin, title=title, images=images, videos=videos, variations=variations,
                                 current_variation=variation)

            else:  # single product, complete
                twister = re.search(r"var data = ({.+});",
                                    soup.select_one('#imageBlock_feature_div > script:nth-child(3)').string,
                                    re.DOTALL).groups(1)[0]
                twister = '\n'.join(
                    re.findall(r'''^["'](?:colorImages|colorToAsin|heroImage|heroVideo)["'].+$''', twister,
                               re.MULTILINE))
                twister = '{' + twister + '}'
                image, twister = to_json(image), to_json(twister)

                title = html.unescape(image['title'])
                images = [ProductImage.from_json(data) for data in twister['colorImages']['initial']]
                hero_images = [ProductImage.from_json(data) for data in twister['heroImage']['initial']]
                videos = [Video.from_json(data) for data in image['videos']]
                hero_videos = [Video.from_json(data) for data in image.get('heroVideo', [])]

                return Product(asin=asin, title=title, variation=[], images=images, videos=videos,
                               hero_images=hero_images, hero_videos=hero_videos)
        elif soup.select('#ebooksImgBlkFront'):  # kindle book? complete
            variations, variation = self._get_media_variations(soup, asin)

            img = soup.select_one('#ebooksImgBlkFront')
            sorted_img = sorted(json.loads(img['data-a-dynamic-image']).items(), key=lambda x: x[1])
            thumb, (img_url, (width, height)) = sorted_img[0][0], sorted_img[-1]
            img = MediaImage(img_url, thumb, width, height)
            title = soup.select_one('#productTitle').text.strip()
            if soup.select_one('#productSubtitle'):
                title = '{} {}'.format(title, soup.select_one('#productSubtitle').text.strip())
            return Kindle(asin, title, img, variations, variation)
        elif soup.select('#a-page > div.av-page-desktop.avu-retail-page > script:nth-child(9)'):  # prime video
            data = soup.select_one('#a-page > div.av-page-desktop.avu-retail-page > script:nth-child(9)')
            data = json.loads(data.string)

            entity_type = list(data['props']['state']['detail']['headerDetail'].values())[0]['entityType']
            if entity_type in ('Movie', 'TV Show'):
                base_asin = data['initArgs']['titleID']
                realm = data['initArgs']['realm']
                locale, territory = data['initArgs']['context']['locale'], data['initArgs']['context'][
                    'recordTerritory']
                svod = list(data['props']['state']['action']['atf'].values())[0]['acquisitionActions'].get(
                    'svodWinners')
                title = list(data['props']['state']['detail']['headerDetail'].values())[0].get('parentTitle') or \
                        list(data['props']['state']['detail']['headerDetail'].values())[0].get('title')
                more_way = list(data['props']['state']['action']['atf'].values())[0]['acquisitionActions'].get(
                    'moreWaysToWatch')

                option_values = []

                if svod:
                    option_values.append(PrimeVideoOption(base_asin, True, '', '', ''))
                if more_way:
                    for op in more_way['children']:
                        for child in op['children']:
                            if child.get('sType') != 'PRIME':
                                asin = child['asin']
                                purchase_type, *_, price = child['label'].split(' ')
                                video_quality = child['purchaseData']['videoQuality']
                                option_values.append(PrimeVideoOption(asin, True, purchase_type, price, video_quality))

            if entity_type == 'Movie':  # movie
                return PrimeVideoMovie(asin, title, option_values, realm, locale, territory)
            elif entity_type == 'TV Show':  # tv show
                seasons: List[PrimeVideoTVSeason] = [PrimeVideoTVSeason.from_json(k, v) for k, v in
                                                     data['props']['state']['detail']['detail'].items()]
                return PrimeVideoTV(asin, title, option_values, seasons, realm, locale, territory)
            else:
                raise TypeError("unknown entity_type `{}`. Maybe an unavailable product.".format(entity_type))

        raise TypeError('unknown product type')

    @retry
    def get_rating(self, asin: str) -> Dict[int, int]:
        resp = self.get_with_update_cookie(self._url_rating(asin))
        if resp.status_code != 200:
            raise ValueError("status code `{}` seems like invalid for `get_rating`".format(resp.status_code))
        soup = BeautifulSoup(resp.text, 'lxml')
        return {i: int(elem[selector.Rating.DataName].rstrip('%')) for elem, i in
                zip(soup.select(selector.Rating.Value), range(5, 0, -1))}

    @retry
    def get_offers(self, asin: str, prime_eligible=False, free_shipping=False, new=False, used_like_new=False,
                   used_very_good=False, used_good=False, used_acceptable=False, merchant=None, page=1) -> OfferList:
        resp = self.get_with_update_cookie(
            self._url_offers(asin, prime_eligible=prime_eligible, free_shipping=free_shipping, new=new,
                             used_like_new=used_like_new, used_very_good=used_very_good, used_good=used_good,
                             used_acceptable=used_acceptable, merchant=merchant, page=page))
        if resp.status_code != 200:
            raise ValueError("status code `{}` seems like invalid for `get_offers`".format(resp.status_code))
        soup = BeautifulSoup(resp.text, 'lxml')
        product_name = soup.select_one(selector.Offer.ProductName).text.strip()
        offer_count = (bool(soup.select_one(selector.Offer.Pinned)) +
                       int(find_number(soup.select_one(selector.Offer.Count).text + '0')))
        offers = []
        for offer in soup.select(selector.Offer.PinnedOffer) + soup.select(selector.Offer.Offers):
            (price, price_fraction, currency,
             rating, heading, ships_from, sold_by) = (offer.select_one(selector.Offer.Price),
                                                      offer.select_one(selector.Offer.PriceFraction),
                                                      offer.select_one(selector.Offer.PriceSymbol),
                                                      offer.select_one(selector.Offer.SellerRating),
                                                      offer.select_one(selector.Offer.Heading),
                                                      offer.select_one(selector.Offer.ShipsFrom),
                                                      offer.select_one(selector.Offer.SoldBy))
            if not price:
                continue
            if price_fraction:
                price = float(find_number(price.text.replace(',', '')) + find_number(price_fraction.text))
            else:
                price = int(find_number(price.text.replace(',', '')))

            currency = currency.text
            heading = remove_whitespace(heading.text)
            ships_from = ships_from.text.strip()
            if sold_by.name == 'a':
                sold_by_url = self._abs_path(sold_by['href'])
            else:
                sold_by_url = None
            sold_by = sold_by.text.strip()

            if rating:
                for cls in rating['class']:
                    if cls.startswith(selector.Offer.StarClassPrefix):
                        cls = cls.lstrip(selector.Offer.StarClassPrefix)
                        rating = float(cls.replace('-', '.'))
                        break

            offers.append(Offer(price=price, currency=currency, rating=rating,
                                condition=heading, ships_from=ships_from, sold_by=sold_by, sold_by_url=sold_by_url))
        return OfferList(product_name, offer_count, offers,
                         settings={"prime_eligible": prime_eligible, "free_shipping": free_shipping, "new": new,
                                   "used_like_new": used_like_new, "used_very_good": used_very_good,
                                   "used_good": used_good,
                                   "used_acceptable": used_acceptable, "merchant": merchant, "page": page})

    @retry
    def get_review(self, asin: str, page=1, setting: ReviewSettings = ReviewSettings()) -> ReviewList:

        resp = self.post_with_update_cookie(self._url_reviews(page), data=setting.to_dict(asin))
        review = []

        for dat in resp.text.split(selector.Review.StreamStrip):
            if not dat:
                continue
            data = eval(dat)
            if data[0] == selector.Review.StreamIndex0 and data[2]:
                soup = BeautifulSoup(data[2], 'lxml')
                top = soup.select_one(selector.Review.StreamTop)
                if top and top.get(selector.Review.DataAttr, None) == selector.Review.ReviewDataAttr:
                    rating = top.select_one(selector.Review.RatingIcon)

                    if rating:
                        for cls in rating['class']:
                            if cls.startswith(selector.Review.StarClassPrefix):
                                cls = cls.lstrip(selector.Review.StarClassPrefix)
                                rating = int(cls)
                                break

                    title = top.select_one(selector.Review.Title)
                    if title:
                        title = title.text.strip()

                    helpful = top.select_one(selector.Review.Helpful)
                    if helpful:
                        try:
                            helpful = int(find_number(helpful.text.strip()))
                        except ValueError:  # 'One person found this helpful'
                            helpful = 1
                    else:
                        helpful = 0

                    body = top.select_one(selector.Review.Body)
                    if body:
                        body = body.text.strip()

                    reviewer = top.select_one(selector.Review.Reviewer)
                    reviewer_url = top.select_one(selector.Review.ReviewerURL)
                    if reviewer:
                        reviewer = reviewer.text.strip()
                    if reviewer_url:
                        reviewer_url = self._abs_path(reviewer_url['href'])

                    review_url = top.select_one(selector.Review.ReviewURL)
                    if review_url:
                        review_url = self._abs_path(review_url['href'])

                    review.append(Review(reviewer, reviewer_url, review_url, title, rating, helpful, body))
        return ReviewList(review, asin, self.country, setting, len(review) != setting.page_size)

    @retry
    def search(self, keyword: str, page: int = None, min_price: int = None, max_price: int = None, merchant: str = None,
               category: SearchCategory = None):
        """
        :param keyword: Keyword to search
        :param page: page number
        :param min_price: minimum price to show
        :param max_price: maximum price to show
        :param merchant: merchantID. or, "amazon" to Amazon's Merchant ID in Current Region.
        :param category: Category to search
        :return:
        """

        resp = self.get_with_update_cookie(self._url_search(keyword, page, min_price, max_price, merchant, category))
        soup = BeautifulSoup(resp.text, 'lxml')
        result = []
        for item in soup.select('div.s-result-item.s-asin'):
            asin = item['data-asin']
            name = item.select_one('h2 > a > span').string

            price, price_fraction, currency = (item.select_one(selector.Offer.Price),
                                               item.select_one(selector.Offer.PriceFraction),
                                               item.select_one(selector.Offer.PriceSymbol))
            if price:
                if price_fraction:
                    price = float(find_number(price.text.replace(',', '')) + find_number(price_fraction.text))
                else:
                    price = int(find_number(price.text.replace(',', '')))

                currency = currency.text
            options = []

            for option in item.select(
                    'div.a-section > div.sg-row:nth-child(2) > div.sg-col:nth-child(2) >* div.a-section >* div.a-section'):
                if 'a-spacing-top-small' in option['class'] or 'a-spacing-top-mini' in option['class']:
                    option_name = option.select_one('a.a-text-bold')
                    if option_name:
                        option_name = option_name.string

                    _asin = option.select_one('a')
                    if 's-sponsored-label-text' in _asin['class']:
                        continue
                    if _asin:
                        _asin = parse_asin_from_url(_asin['href'])

                    _price, _price_fraction, _currency = (option.select_one(selector.Offer.Price),
                                                          option.select_one(selector.Offer.PriceFraction),
                                                          option.select_one(selector.Offer.PriceSymbol))
                    if _price:
                        if _price_fraction:
                            _price = float(find_number(_price.text.replace(',', '')) +
                                           find_number(_price_fraction.text))
                        else:
                            _price = int(find_number(_price.text.replace(',', '')))
                        _currency = _currency.string
                    if any([_asin, option_name, _price, _currency]):
                        options.append(SearchResultProductOffers(_asin, option_name, _currency, _price))
            price = min([price] + [p.price for p in options])
            result.append(SearchResultProduct(asin, name, currency, price, options))

        return SearchResult(result, keyword, page or 1, min_price, max_price, merchant, category)

    def _url_top_page(self) -> str:
        return self._abs_path('')

    def _url_product(self, asin: str) -> str:
        return self._abs_path('/dp/{asin}'.format(asin=asin))

    def _url_offers(self, asin: str, prime_eligible, free_shipping, new, used_like_new,
                    used_very_good, used_good, used_acceptable, merchant: str = None, page=1) -> str:
        filter_query = []
        if not (new and used_like_new and used_very_good and used_good and used_acceptable):
            for flag, name in [(new, 'new'), (used_like_new, 'usedLikeNew'), (used_very_good, 'usedVeryGood'),
                               (used_good, 'usedGood'), (used_acceptable, 'usedAcceptable')]:
                if flag:
                    filter_query.append(name)
        for flag, name in [(prime_eligible, 'primeEligible'), (free_shipping, 'freeShipping')]:
            if flag:
                filter_query.append(name)

        filter_query = quote(json.dumps({name: True for name in filter_query})) if filter_query else ''

        if merchant:
            return self._abs_path('/gp/aod/ajax/ref=auto_load_aod?asin={asin}&pc=dp&pageno={page}&m={merchant}' \
                                  '{filter}'.format(asin=asin, page=page, merchant=merchant,
                                                    filter='&filter={}'.format(filter_query) if filter_query else ''))
        return self._abs_path('/gp/aod/ajax/ref=auto_load_aod?asin={asin}&pc=dp&' \
                              'pageno={page}{filter}'.format(asin=asin, page=page,
                                                             filter='&filter={}'.format(
                                                                 filter_query) if filter_query else ''))

    def _url_rating(self, asin: str) -> str:
        return self._abs_path('/gp/customer-reviews/widgets/average-customer-review/' \
                              'popover/ref=dpx_acr_pop_?contextId=dpx&asin={asin}'.format(asin=asin))

    def _url_reviews(self, page=1) -> str:
        return self._abs_path('/hz/reviews-render/ajax/reviews/get/' \
                              'ref=cm_cr_getr_d_paging_btm_next_{page}'.format(page=page))

    def _url_search(self, keyword: str, page: int, min_price: int, max_price: int, merchant: str,
                    category: SearchCategory):
        query = ['k={}'.format(keyword)]
        if min_price:
            query.append('low-price={}'.format(min_price))
        if max_price:
            query.append('high-price={}'.format(max_price))
        if merchant:
            if merchant == 'amazon':
                query.append('emi={}'.format(self.country.amazon_merchant_id))
            else:
                query.append('emi={}'.format(merchant))
        if category:
            query.append('i={}'.format(category.value_by_country(self.country)))
        if page:
            query.append('page={}'.format(page))
        return self._abs_path('/s?' + '&'.join(query))

    def _create_header(self):
        return {**self.headers, 'cookie': '; '.join(f'{k}={v}' for k, v in self.cookie.items())}

    def _abs_path(self, endpoint: str) -> str:
        return urljoin('https://{}'.format(self.domain), endpoint)

    def _get_media_variations(self, soup: BeautifulSoup, asin: str) -> Tuple[List[MediaVariation],
                                                                             Optional[MediaVariation]]:

        variations: List[MediaVariation] = []
        variation = None
        types, values = (soup.select('li.swatchElement > span > span > span > a > span:first-child'),
                         soup.select('li.swatchElement > span > span > span > a > span > span.a-size-base'))
        if not types:
            warn("looks like terraplen couldn't get proper html")
        for type_, value in zip(types, values):
            if 'a-color-price' in value['class']:
                _asin = asin
            else:
                _asin = type_.parent['href'].rsplit('/')[-2]
            val = MediaVariation(type_.text.strip(), value.text.strip(), _asin)
            if 'a-color-price' in value['class']:
                variation = val
            variations.append(val)
        return variations, variation
