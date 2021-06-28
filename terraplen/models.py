from enum import Enum
from typing import List, Dict, Union


class UserAgents:
    def __init__(self, head: str, version: List[str]):
        self.head = head
        self.version = version

        self.index = -1

    def get_next_user_agent(self):
        self.index = (self.index + 1) % len(self.version)
        return '{head} {version}'.format(head=self.head, version=self.version[self.index])


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
    def __init__(self, offer_count: int, offers: List[Offer]):
        self.offer_count = offer_count
        self.offers = offers

    def __repr__(self):
        offers_repr_length = 100
        offers_repr = repr(self.offers)
        print_offers = offers_repr[:offers_repr_length]
        if offers_repr[offers_repr_length:]:
            print_offers += '...'
        return 'OfferList(offer_count={}, offers={})'.format(self.offer_count, print_offers)


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
    def __init__(self, reviews: List[Review], asin: str, country: Country, settings: Dict, page=1, last_page=False):
        self.reviews = reviews
        self.asin = asin
        self.country = country
        self.settings = settings
        self.page = page
        self.last_page = last_page

    def __repr__(self):
        reviews_repr_length = 100
        reviews_repr = repr(self.reviews)
        print_reviews = reviews_repr[:reviews_repr_length]
        if reviews_repr[reviews_repr_length:]:
            print_reviews += '...'
        return 'ReviewList(reviews={}, asin={}, country={}, page={}, last_page={})'.format(print_reviews,
                                                                                           self.asin, self.country,
                                                                                           self.page, self.last_page)
