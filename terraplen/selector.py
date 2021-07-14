class Rating:
    Value = 'div.a-meter'
    DataName = 'aria-valuenow'


class Offer:
    ProductName = '#aod-asin-title-text'

    Pinned = '#aod-pinned-offer >* input.a-button-input'
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
    ImageJS = '#imageBlockVariations_feature_div > script'
    ImageJSRe = r"var obj = jQuery\.parseJSON\('([^']+)'\);"
    TwisterContainerId = '#twisterContainer'
    TwisterJSSelector = '#twisterJsInitializer_feature_div > script'
    TwisterJSRe = r"var dataToReturn = ([^;]+)"
    TwisterJSRemoveRe = r'"updateDivLists"\s*:\s*{([^}[]+\[[^]]*\],?\s*)+},'

    VariationLabels = 'variationDisplayLabels'
    VisualDimensions = 'visualDimensions'
    Dimension = 'dimensions'
    DimensionToAsin = 'dimensionToAsinMap'
    Title = 'title'
    DimensionDisplay = 'dimensionsDisplay'
    VariationValues = 'variationValues'
    Videos = 'videos'
    ParentAsin = 'parentAsin'
    ColorImages = 'colorImages'
    HeroImages = 'heroImages'
    HeroImage = 'heroImage'
    HeroVideo = 'heroVideo'
    ColorToAsin = 'colorToAsin'
    Asin = 'asin'
    LandingAsinColor = 'landingAsinColor'

    BookSwitches = '#tmmSwatches'
    BookTwister = '#booksImageBlock_feature_div > script:nth-child(2)'
    BookTwisterContentRe = r'''^["']imageGalleryData["'].+$'''

    ImageGalleryData = 'imageGalleryData'

    MovieTwister = '#imageBlock_feature_div > script:nth-child(3)'
    MovieTwisterRe = r"var data = ({.+});"
    MovieTwisterContentRe = r'''^["'](?:colorImages|colorToAsin|heroImage|heroVideo)["'].+$'''

    Initial = 'initial'

    ProductTwister = '#imageBlock_feature_div > script:nth-child(3)'
    ProductTwisterRe = r"var data = ({.+});"
    ProductTwisterContentRe = r'''^["'](?:colorImages|colorToAsin|heroImage|heroVideo)["'].+$'''

    KindleSelector = '#ebooksImgBlkFront'
    KindleDynamicImage = 'data-a-dynamic-image'
    KindleTitle = '#productTitle'
    KindleSubTitle = '#productSubtitle'

    PrimeVideoData = '#a-page > div.av-page-desktop.avu-retail-page > script:nth-child(9)'

    PrimeProps = 'props'
    PrimeState = 'state'
    PrimeDetail = 'detail'
    PrimeHeaderDetail = 'headerDetail'

    PrimeEntityType = 'entityType'
    PrimeInitArgs = 'initArgs'
    PrimeTitleId = 'titleID'
    PrimeRealm = 'realm'

    PrimeAcquisition = 'acquisitionActions'
    PrimeSVOD = 'svodWinners'

    PrimeParentTitle = 'parentTitle'
    PrimeTitle = 'title'

    PrimeContext = 'context'
    PrimeLocale = 'locale'
    PrimeRecordTerritory = 'recordTerritory'
    PrimeAction = 'action'
    PrimeAtf = 'atf'
    PrimeMoreWaysToWatch = 'moreWaysToWatch'

    PrimeMoreWayChildren = 'children'
    PrimeOptionType = 'sType'
    PrimeTypeName = 'PRIME'

    PrimeAsin = 'asin'

    PrimeDescTest = 'label'

    PrimePurchaseData = 'purchaseData'
    PrimeVideoQuality = 'videoQuality'


class Variation:
    Types = 'li.swatchElement > span > span > span > a > span:first-child'
    Values = 'li.swatchElement > span > span > span > a > span > span.a-size-base'

    ValidClass = 'a-color-price'
