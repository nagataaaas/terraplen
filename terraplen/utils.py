import re


def find_number(text: str) -> float:
    try:
        return float(re.findall(r'\d(?:[\d,.]*\d)?', text)[0].replace(',', ''))
    except IndexError:
        raise ValueError("Seems like there is no numbers in `{}`".format(text))


def remove_whitespace(text: str) -> str:
    return re.sub(r'\s+', '', text)
