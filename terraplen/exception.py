BotDetectedStatusCode = 503
ProductNotFoundCode = 404


class DetectedAsBotException(RuntimeError):
    pass


class ProductNotFoundException(ValueError):
    pass
