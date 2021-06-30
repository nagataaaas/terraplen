import re
from typing import Tuple


def find_number(text: str) -> float:
    try:
        return float(re.findall(r'\d(?:[\d,.]*\d)?', text)[0].replace(',', ''))
    except IndexError:
        raise ValueError("Seems like there is no numbers in `{}`".format(text))


def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', '', text)


def thumb_size(url: str) -> Tuple[int, int]:
    match = re.match(r'https://m.media-amazon.com/images/I/[^.]+\.SX(\d+)_SY(\d+)_[^.]+\.png', url)
    return int(match.group(1)), int(match.group(2))