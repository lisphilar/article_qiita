#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import json
import re
from xml.etree import ElementTree
import requests


class LawLoader(object):
    """
    Prepare law data with e-Gov (https://www.e-gov.go.jp/) site.

    Args:
        category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)
    """

    def __init__(self, category=1):
        self.law_dict = self._get_law_dict(category=category)
        self.content_dict = {}

    @staticmethod
    def _get_xml(url):
        """
        Get XML data from e-Gov API.

        Args:
            url (str): key of the API

        Returns:
            xml.ElementTree: element tree of the XML data
        """
        r = requests.get(url)
        return ElementTree.fromstring(r.content.decode(encoding="utf-8"))

    def _get_law_dict(self, category):
        """
        Return dictionary of law names and numbers.

        Args:
            category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)

        Returns:
            dict(str, str): dictionary of law names (keys) and numbers (values)
        """
        url = f"https://elaws.e-gov.go.jp/api/1/lawlists/{category}"
        root = self._get_xml(url)
        names = [e.text for e in root.iter() if e.tag == "LawName"]
        numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
        return {name: num for (name, num) in zip(names, numbers)}

    def get_law_number(self, keyword, category=1):
        """
        Return the law number.
        This will be retrieved from e-Gov (https://www.e-gov.go.jp/)

        Args:
            keyword (str): keyword of the law name
            category (int): category number, like 1 (all), 2 (法令), 3 (政令), 4 (省令)

        Returns:
            dict(str, str): dictionary of law name (key) and law number (value)
        """
        return {k: v for (k, v) in self.law_dict.items() if keyword in k}

    def get_raw(self, number):
        """
        Args:
            number (str): Number of the law, like '平成九年厚生省令第二十八号'

        Returns:
            raw (list[str]): raw contents of J-GCP
        """
        if number in self.content_dict:
            return self.content_dict[number]
        url = f"https://elaws.e-gov.go.jp/api/1/lawdata/{number}"
        root = self._get_xml(url)
        contents = [e.text.strip() for e in root.iter() if e.text]
        raw = [t for t in contents if t]
        self.content_dict = {number: raw}
        return raw

    @staticmethod
    def pre_process(raw):
        """
        Perform pre-processing on raw contents.

        Args:
            raw (list[str]): raw contents

        Returns:
            str: pre-processed string

        Notes:
            - Strings enclosed with （ and ） will be removed.
            - 「 and 」 will be removed.
        """
        contents = [s for s in raw if s.endswith("。")]
        string = "".join(contents)
        string = string.translate(str.maketrans({"「": "", "」": ""}))
        return re.sub("（[^（|^）]*）", "", string)

    def gcp(self):
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
        number_dict = self.get_law_number("医薬品の臨床試験")
        number = number_dict["医薬品の臨床試験の実施の基準に関する省令"]
        raw = self.get_raw(number)
        raw_without56 = raw[: raw.index("第五十六条")]
        return self.pre_process(raw_without56)


def main():
    # The Constitution of Japan
    loader2 = LawLoader(category=2)
    consti_number = loader2.get_law_number("日本国憲法")
    print(consti_number)
    consti_raw = loader2.get_raw("昭和二十一年憲法")
    consti = loader2.pre_process(consti_raw)
    # J-GCP
    loader4 = LawLoader(category=4)
    gcp = loader4.gcp()
    # Results
    result_dict = {
        "日本国憲法": consti,
        "J-GCP": gcp,
    }
    with codecs.open("law.json", "w", encoding="utf-8") as fh:
        json.dump(result_dict, fh, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
