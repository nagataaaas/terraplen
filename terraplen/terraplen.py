import requests
from enum import Enum
from typing import List, Tuple

from terraplen.wrappers import retry
from terraplen.exception import DetectedAsBotException, BotDetectedStatusCode, ProductNotFoundCode, \
    ProductNotFoundException
from terraplen.utils import find_number, remove_whitespace

from bs4 import BeautifulSoup
import json
from urllib.parse import quote, urljoin


# amazon returns 503 if predicted as a bot

class UserAgents:
    def __init__(self, head: str, version: List[str]):
        self.head = head
        self.version = version

        self.index = -1

    def get_next_user_agent(self):
        self.index = (self.index + 1) % len(self.version)
        return '{head} {version}'.format(head=self.head, version=self.version[self.index])


class Selector:
    class Rating:
        Value = 'div.a-meter'
        DataName = 'aria-valuenow'

    class Offer:
        Pinned = '#a-autoid-2'
        Count = '#aod-filter-offer-count-string'
        Price = 'span.a-price-whole'
        PriceFraction = 'span.a-price-fraction'
        PriceSymbol = 'span.a-price-symbol'
        SellerRating = '#aod-offer-seller-rating > i'
        Heading = '#aod-offer-heading'

        PinnedOffer = '#aod-pinned-offer'
        Offers = '#aod-offer'
        StarClassPrefix = 'a-star-mini-'

    class Review:
        StreamStrip = '\n&&&\n'
        StreamIndex0 = 'append'
        StreamTop = 'div'
        DataAttr = 'data-hook'
        ReviewDataAttr = 'review'
        RatingIcon = 'i.review-rating'
        StarClassPrefix = 'a-star-'

        ReviewURL = 'a.a-link-normal.review-title'
        Title = 'a[data-hook="review-title"]'
        Helpful = 'span[data-hook="helpful-vote-statement"]'
        Body = 'span[data-hook="review-body"]'
        Reviewer = 'span.a-profile-name'
        ReviewerURL = 'a.a-profile'


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


class Offer:
    def __init__(self, price: float, currency: str, rating: float, condition: str):
        self.price = price
        self.currency = currency
        self.approx_review = rating
        self.condition = condition

    def __repr__(self):
        return 'Offer(price={}, currency="{}", approx_review={}, condition="{}")'.format(self.price, self.currency,
                                                                                         self.approx_review,
                                                                                         self.condition)


class Review:
    def __init__(self, reviewer: str, reviewer_url: str, review_url: str, title: str, rating: int, helpful: int, body: str):
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


class AllOffer:
    def __init__(self, offer_count: int, offers: List[Offer]):
        self.offer_count = offer_count
        self.offers = offers

    def __repr__(self):
        offers_repr_length = 100
        offers_repr = repr(self.offers)
        print_offers = offers_repr[:offers_repr_length]
        if offers_repr[offers_repr_length:]:
            print_offers += '...'
        return 'AllOffer(offer_count={}, offers={})'.format(self.offer_count, print_offers)


class Scraper:
    user_agents = UserAgents('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
                             ['Chrome/91.0.4472.106 Safari/537.36', 'Chrome/91.0.4472.77 Safari/537.36',
                              'Chrome/91.0.4472.114 Safari/537.36', 'Chrome/91.0.4472.101 Safari/537.36',
                              'Chrome/91.0.4472.124 Safari/537.36'])

    def __init__(self, country: Country = Country.UnitedStates, run_init=True):
        """
        Create Scraper Instance
        :param country: Instance of `terraplen.Country` or `str`
        :param run_init: Whether run first setup. setup accesses to Amazon homepage.
        """
        if isinstance(country, Country):
            self.country = country
        elif isinstance(country, str):
            self.country = Country(country)  # This will raise `ValueError` if `country` is invalid.

        self.domain = 'www.amazon.{}'.format(self.country.value)
        self.headers = {'User-Agent': self.user_agents.get_next_user_agent()}
        self.cookie = {}
        self.init_have_run = False

        if run_init:
            self.init()

    def init(self):
        self.get_with_update_cookie(self._url_top_page())

    def get_with_update_cookie(self, url: str) -> BeautifulSoup:
        resp = requests.get(url, headers=self._create_header())
        if resp.status_code == DetectedAsBotException:
            raise BotDetectedStatusCode
        if resp.status_code == ProductNotFoundCode:
            raise ProductNotFoundException
        self.cookie.update(resp.cookies)
        return BeautifulSoup(resp.text, 'lxml')


    # TODO: post_with_update_cookie

    @retry
    def get_rating(self, asin: str):
        soup = self.get_with_update_cookie(self._url_rating(asin))
        return {i: int(elem[Selector.Rating.DataName].rstrip('%')) for elem, i in
                zip(soup.select(Selector.Rating.Value), range(5, 0, -1))}

    @retry
    def get_offers(self, asin: str, prime_eligible=False, free_shipping=False, new=False, used_like_new=False,
                   used_very_good=False, used_good=False, used_acceptable=False, merchant=None, page=1):

        soup = self.get_with_update_cookie(
            self._url_offers(asin, prime_eligible=prime_eligible, free_shipping=free_shipping, new=new,
                             used_like_new=used_like_new, used_very_good=used_very_good, used_good=used_good,
                             used_acceptable=used_acceptable, merchant=merchant, page=1))

        offer_count = (bool(soup.select(Selector.Offer.Pinned)) +
                       int(find_number(soup.select_one(Selector.Offer.Count).text + '0')))
        offers = []
        for offer in soup.select(Selector.Offer.PinnedOffer) + soup.select(Selector.Offer.Offers):
            price, price_fraction, currency, rating, heading = (offer.select_one(Selector.Offer.Price),
                                                                offer.select_one(Selector.Offer.PriceFraction),
                                                                offer.select_one(Selector.Offer.PriceSymbol),
                                                                offer.select_one(Selector.Offer.SellerRating),
                                                                offer.select_one(Selector.Offer.Heading))
            if price_fraction:
                price = float(price.text.replace(',', '') + price_fraction.text)
            else:
                price = int(price.text.replace(',', ''))

            if rating:
                for cls in rating['class']:
                    if cls.startswith(Selector.Offer.StarClassPrefix):
                        cls = cls.lstrip(Selector.Offer.StarClassPrefix)
                        rating = float(cls.replace('-', '.'))
                        break

            offers.append(Offer(price=price, currency=currency.text, rating=rating,
                                condition=remove_whitespace(heading.text)))
        return AllOffer(offer_count, offers)

    def _url_top_page(self) -> str:
        return 'https://{domain}'.format(domain=self.domain)

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
            return 'https://{domain}/gp/aod/ajax/ref=auto_load_aod?' \
                   'asin={asin}&pc=dp&pageno={page}&m={merchant}' \
                   '{filter}'.format(domain=self.domain,
                                     asin=asin,
                                     page=page,
                                     merchant=merchant,
                                     filter='&filter={}'
                                     .format(
                                         filter_query) if filter_query else '')
        return 'https://{domain}/gp/aod/ajax/ref=auto_load_aod?' \
               'asin={asin}&pc=dp&pageno={page}{filter}'.format(domain=self.domain,
                                                                asin=asin,
                                                                page=page,
                                                                filter='&filter={}'.
                                                                format(filter_query) if
                                                                filter_query else '')

    def _url_rating(self, asin: str) -> str:
        return 'https://{domain}/gp/customer-reviews/widgets/average-customer-review/' \
               'popover/ref=dpx_acr_pop_?contextId=dpx&asin={asin}'.format(domain=self.domain, asin=asin)

    def _url_reviews(self, asin: str) -> str:
        return 'https://{domain}/product-reviews/{asin}/ref=cm_cr_othr_d_show_all_btm' \
               '?ie=UTF8&reviewerType=all_reviews'.format(domain=self.domain, asin=asin)

    def _url_reviews2(self, page=1) -> str:
        return 'https://{domain}/hz/reviews-render/ajax/reviews/get/' \
               'ref=cm_cr_getr_d_paging_btm_next_{page}'.format(domain=self.domain, page=page)

    def get_review(self, asin: str, page=1) -> Tuple[List[Review], bool]:  # Should I add some `settings`?

        page_size = 10

        resp = requests.post(self._url_reviews2(page), data={'sortBy': 'recent',  # 'recent' or 'helpful'(default)
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
                                                             'scope': 'reviewsAjax1'},
                             headers=self._create_header())
        review = []

        for dat in resp.text.split(Selector.Review.StreamStrip):
            if not dat:
                continue
            data = eval(dat)
            if data[0] == Selector.Review.StreamIndex0 and data[2]:
                soup = BeautifulSoup(data[2], 'lxml')
                top = soup.select_one(Selector.Review.StreamTop)
                if top and top.get(Selector.Review.DataAttr, None) == Selector.Review.ReviewDataAttr:
                    rating = top.select_one(Selector.Review.RatingIcon)

                    if rating:
                        for cls in rating['class']:
                            if cls.startswith(Selector.Review.StarClassPrefix):
                                cls = cls.lstrip(Selector.Review.StarClassPrefix)
                                rating = int(cls)
                                break

                    title = top.select_one(Selector.Review.Title)
                    if title:
                        title = title.text.strip()

                    helpful = top.select_one(Selector.Review.Helpful)
                    if helpful:
                        try:
                            helpful = int(find_number(helpful.text.strip()))
                        except ValueError:  # 'One person found this helpful'
                            helpful = 1
                    else:
                        helpful = 0

                    body = top.select_one(Selector.Review.Body)
                    if body:
                        body = body.text.strip()

                    reviewer = top.select_one(Selector.Review.Reviewer)
                    reviewer_url = top.select_one(Selector.Review.ReviewerURL)
                    if reviewer:
                        reviewer = reviewer.text.strip()
                    if reviewer_url:
                        reviewer_url = self._abs_path(reviewer_url['href'])

                    review_url = top.select_one(Selector.Review.ReviewURL)
                    if review_url:
                        review_url = self._abs_path(review_url['href'])

                    review.append(Review(reviewer, reviewer_url, review_url, title, rating, helpful, body))
        return review, len(review) != page_size

    def _create_header(self):
        return {**self.headers, 'cookie': '; '.join(f'{k}={v}' for k, v in self.cookie.items())}

    def _abs_path(self, endpoint: str) -> str:
        return urljoin('https://{}'.format(self.domain), endpoint)
