"""
    TODO: Change
    terraplen
    ===

    Easy and Useful Amazon Scraper

    Powered by [Yamato Nagata](https://twitter.com/514YJ)
    [GitHub](https://github.com/nagataaaas/terraplen)
    :copyright: (c) 2021 by Yamato Nagata.
    :license: MIT.
"""

import locale

from .__about__ import __version__
from .terraplen import (Scraper, Country)

locale.setlocale(locale.LC_ALL, '')

__all__ = [
    "__version__",
    "Scraper",
    "Country"
]
