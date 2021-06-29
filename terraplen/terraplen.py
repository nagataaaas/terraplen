import requests

from terraplen import selector
from terraplen.wrappers import retry
from terraplen.exception import (DetectedAsBotException, BotDetectedStatusCode,
                                 ProductNotFoundCode, ProductNotFoundException)
from terraplen.utils import find_number, remove_whitespace
from terraplen.models import (Offer, OfferList, Review, ReviewList, Country, UserAgents, Currency, Language)

from bs4 import BeautifulSoup
import json
from urllib.parse import quote, urljoin
from typing import Dict, Optional
import re

from warnings import warn


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
            language = country.lang_and_currency()[0]
        if not currency:
            currency = country.lang_and_currency()[1]

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
    def _language_cookie_key(self):
        if self.country == Country.UnitedStates:
            return 'lc-main'
        else:
            return 'lc-acb{}'.format(self.country.value.split('.')[-1])

    @retry
    def get_product(self, asin: str):
        resp = self.get_with_update_cookie(self._url_product(asin))
        soup = BeautifulSoup(resp.text, 'lxml')
        image_block = re.search(r"var obj = jQuery\.parseJSON\('([^']+)'\);",
                                soup.select_one(
                                    '#imageBlockVariations_feature_div > script').string).groups(1)[0]
        if soup.select('#twisterContainer'):  # has options
            print('twisting!')
            twister = soup.select_one('#twisterJsInitializer_feature_div > script')
            twister = re.search(r"var dataToReturn = ([^;]+)", twister.string).groups(1)[0]
            twister = re.sub(r'"updateDivLists"\s*:\s*{([^}[]+\[[^]]*\],?\s*)+},', '', twister,
                             1)  # this is much faster
        else:
            print('not twisting...')
            twister = re.search(r"var data = ({.+});",
                                soup.select_one('#imageBlock_feature_div > script:nth-child(3)').string,
                                re.DOTALL).groups(1)[0]
            twister = '\n'.join(
                re.findall(r'''^["'](?:colorImages|colorToAsin|heroImage)["'].+$''', twister, re.MULTILINE))
            twister = '{' + twister + '}'

        return image_block, twister

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
                price = float(price.text.replace(',', '') + price_fraction.text)
            else:
                price = int(price.text.replace(',', ''))

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
    def get_review(self, asin: str, page=1) -> ReviewList:  # Should I add some `settings`?

        page_size = 10

        settings = {'sortBy': 'recent',  # 'recent' or 'helpful'(default)
                    'reviewerType': 'all_reviews',
                    # 'avp_only_reviews' (Verified purchase) or
                    # 'all_reviews'(default)
                    'formatType': '',
                    # 'current_format' or 'all_formats'(default)
                    'mediaType': '',
                    # 'media_reviews_only' or 'all_contents'(default)
                    'filterByStar': 'all_stars',
                    # {'one', 'two', 'three', 'four', 'five'} + '_star' or
                    # 'positive' or 'critical' or 'all_stars'(default)
                    'pageNumber': page,  # default=1
                    'filterByLanguage': '',
                    'filterByKeyword': '',  # search
                    'shouldAppend': 'undefined',
                    'deviceType': 'desktop',
                    'canShowIntHeader': 'undefined',
                    'reftag': 'cm_cr_getr_d_paging_btm_next_{}'.format(page),
                    'pageSize': page_size,  # default=10, max=20, min=1
                    'asin': asin,
                    'scope': 'reviewsAjax1'}

        resp = self.post_with_update_cookie(self._url_reviews(page), data=settings)
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
        return ReviewList(review, asin, self.country, settings, len(review) != page_size)

    def _url_top_page(self) -> str:
        return 'https://{domain}'.format(domain=self.domain)

    def _url_product(self, asin: str) -> str:
        return 'https://{domain}/dp/{asin}'.format(domain=self.domain, asin=asin)

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
            return 'https://{domain}/gp/aod/ajax/ref=auto_load_aod?asin={asin}&pc=dp&pageno={page}&m={merchant}' \
                   '{filter}'.format(domain=self.domain, asin=asin, page=page, merchant=merchant,
                                     filter='&filter={}'.format(filter_query) if filter_query else '')
        return 'https://{domain}/gp/aod/ajax/ref=auto_load_aod?asin={asin}&pc=dp&' \
               'pageno={page}{filter}'.format(domain=self.domain, asin=asin, page=page,
                                              filter='&filter={}'.format(filter_query) if filter_query else '')

    def _url_rating(self, asin: str) -> str:
        return 'https://{domain}/gp/customer-reviews/widgets/average-customer-review/' \
               'popover/ref=dpx_acr_pop_?contextId=dpx&asin={asin}'.format(domain=self.domain, asin=asin)

    def _url_reviews(self, page=1) -> str:
        return 'https://{domain}/hz/reviews-render/ajax/reviews/get/' \
               'ref=cm_cr_getr_d_paging_btm_next_{page}'.format(domain=self.domain, page=page)

    def _create_header(self):
        return {**self.headers, 'cookie': '; '.join(f'{k}={v}' for k, v in self.cookie.items())}

    def _abs_path(self, endpoint: str) -> str:
        return urljoin('https://{}'.format(self.domain), endpoint)
