#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
from functools import lru_cache
# from pprint import pprint
import re
from xml.etree import ElementTree
import requests


@lru_cache
def get_raw(number):
    """
    Retrieve contents of the law specified with law number from e-Gov API.

    Args:
        number (str): Number of the law, like '平成九年厚生省令第二十八号'

    Returns:
        raw (list[str]): raw contents of J-GCP
    """
    url = f"https://elaws.e-gov.go.jp/api/1/lawdata/{number}"
    r = requests.get(url)
    root = ElementTree.fromstring(r.content.decode(encoding="utf-8"))
    contents = [e.text.strip() for e in root.iter() if e.text]
    return [t for t in contents if t]


def preprocess_gcp(raw):
    """
    Perform pre-processing on raw contents of J-GCP.

    Args:
        raw (list[str]): raw contents of J-GCP

    Returns:
        str: pre-processed string of J-GCP

    Notes:
        - Article 56 will be removed.
        - Strings enclosed with （ and ） will be removed.
        - 「 and 」 will be removed.
    """
    # contents = raw[:]
    # Remove article 56
    contents = raw[: raw.index("第五十六条")]
    # Select sentenses
    contents = [s for s in contents if s.endswith("。")]
    # Join the sentenses
    gcp = "".join(contents)
    # 「 and 」 will be removed
    gcp = gcp.translate(str.maketrans({"「": "", "」": ""}))
    # Strings enclosed with （ and ） will be removed
    return re.sub("（[^（|^）]*）", "", gcp)


def main():
    gcp_raw = get_raw("平成九年厚生省令第二十八号")
    # pprint(gcp_raw, compact=False)
    with codecs.open("gcp_raw.json", "w", encoding="utf-8") as fh:
        json.dump({"gcp": gcp_raw}, fh, indent=4, ensure_ascii=False)
    gcp = preprocess_gcp(gcp_raw)
    # print(gcp)
    with codecs.open("gcp.txt", "w", encoding="utf-8") as fh:
        fh.write(gcp)


if __name__ == "__main__":
    main()
