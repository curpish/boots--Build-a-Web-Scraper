class CrawlerError(Exception):
    """Base exception for all web crawler errors."""

    pass


class RequestFailedError(CrawlerError):
    """Raised when an HTTP request fails or returns an error status code (4xx/5xx)."""

    pass


class InvalidContentTypeError(CrawlerError):
    """Raised when the fetched resource content-type is not text/html."""

    pass
