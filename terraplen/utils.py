import re
from typing import Tuple, Dict, List, Optional
import json


def find_number(text: str) -> float:
    try:
        return float(re.search(r'\d(?:[\d,.]*\d)?', text)[0].replace(',', ''))
    except TypeError:
        raise ValueError("Seems like there is no numbers in `{}`".format(text))


def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', '', text)


def thumb_size(url: str) -> Tuple[int, int]:
    match = re.match(r'https://m.media-amazon.com/images/I/[^.]+\.SX(\d+)_SY(\d+)_[^.]+\.png', url)
    return int(match.group(1)), int(match.group(2))


def to_json(text: str) -> Dict:
    return json.loads(text.replace('\n', '').replace("'", '"').replace(',]', ']').replace(',}', '}'))


def product(categories: List, depth=0):
    current = categories[depth]
    for variation in current.variations:
        if len(categories) > depth + 1:
            for p in product(categories, depth + 1):
                yield [[variation, current.is_visual]] + p
        else:
            yield [[variation, current.is_visual]]


def parse_asin_from_url(url: str) -> Optional[str]:
    try:
        return (re.search('/dp/([^/]+)', url) or re.search('%2Fdp%2F([^%]+)%2F', url))[1]
    except TypeError:
        return None
