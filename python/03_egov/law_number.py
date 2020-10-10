#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
from functools import lru_cache
from pprint import pprint
from xml.etree import ElementTree
import requests


@lru_cache
def get_law_dict(category=1):
    """
    Return dictionary of law names and numbers.
    This will be retrieved from e-Gov (https://www.e-gov.go.jp/)

    Args:
        category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)

    Returns:
        dict(str, str): dictionary of law names (keys) and numbers (values)
    """
    url = f"https://elaws.e-gov.go.jp/api/1/lawlists/{category}"
    r = requests.get(url)
    root = ElementTree.fromstring(r.content.decode(encoding="utf-8"))
    pprint(
        [
            (e.tag, e.text) for e in root.iter() if e.tag in set(["LawName", "LawNo"])
        ][:4], compact=False)
    names = [e.text for e in root.iter() if e.tag == "LawName"]
    numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
    return {name: num for (name, num) in zip(names, numbers)}


def get_law_number(keyword, category=1):
    """
    Return the law number.
    This will be retrieved from e-Gov (https://www.e-gov.go.jp/)

    Args:
        keyword (str): keyword of the law name
        category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)

    Returns:
        dict(str, str): dictionary of law name (key) and law number (value)
    """
    law_dict = get_law_dict(category=category)
    return {k: v for (k, v) in law_dict.items() if keyword in k}


def main():
    # pprint(get_law_dict(category=2), compact=True)
    with codecs.open("law_dict.json", "w", encoding="utf-8") as fh:
        json.dump(get_law_dict(category=2), fh, indent=4, ensure_ascii=False)
    print(get_law_number("日本国憲法", category=2))
    print(get_law_number("著作権", category=2))
    print(get_law_number("医薬品医療機器", category=2))
    print(get_law_number("医薬品の臨床試験", category=4))


if __name__ == "__main__":
    main()
