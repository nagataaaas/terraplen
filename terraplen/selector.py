class Rating:
    Value = 'div.a-meter'
    DataName = 'aria-valuenow'


class Offer:
    ProductName = '#aod-asin-title-text'

    Pinned = '#aod-pinned-offer >* #a-autoid-2'
    Count = '#aod-filter-offer-count-string'
    Price = 'span.a-price-whole'
    PriceFraction = 'span.a-price-fraction'
    PriceSymbol = 'span.a-price-symbol'
    SellerRating = '#aod-offer-seller-rating > i'
    Heading = '#aod-offer-heading'

    PinnedOffer = '#aod-pinned-offer'
    Offers = '#aod-offer'
    StarClassPrefix = 'a-star-mini-'

    ShipsFrom = '#aod-offer-shipsFrom >* span.a-color-base'
    SoldBy = '#aod-offer-soldBy > div > div > div.a-fixed-left-grid-col.a-col-right > *:first-child'


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

class Product:
    ImageLinks = 'li.image.item.maintain-height >* img'