# [Python] e-GOV法令APIより法令本文を取得する

日本の法令データを[e-Gov法令API](https://www.e-gov.go.jp/elaws/pdf/houreiapi_shiyosyo.pdf)より取得し、法令本文を整形する方法についてまとめました。下記Qiita記事を参考にしています。

- [法令APIをGoogle Colab (Python) からアクセスする](https://qiita.com/sakaia/items/c787aa6471e70000d253)
- [e-Gov法令APIとXML　Pythonを用いた特定ワードが含まれる法令条文の抽出](https://qiita.com/kzuzuo/items/d53ff2e092a69424fea0)
- 本文の整形：[【Python3】括弧と括弧内文字列削除](https://qiita.com/mynkit/items/d6714b659a9f595bcac8)

最後の「まとめ」に登場するクラスを含めて、本記事の各コードは[GitHub repository](https://github.com/lisphilar/article_qiita/tree/master/python/03_egov)からダウンロードできます。


## 1. きっかけ
自然言語処理の勉強の題材として、仕事でよく確認している省令（J-GCP, 医薬品の臨床試験の実施の基準に関する省令）を使用したかったというのがきっかけです。Twitterの投稿文などとくらべて分量が少ない点は気になりますが、表記ゆれなどが少ないので自然言語処理の題材としても有用ではないかと思いました。

## 2. 環境
APIへのアクセスに`requests`（pip installが必要）, XMLデータの解析に`xml`パッケージ（標準ライブラリ）を使用します。`functools.lru_cache`は関数出力のキャッシュ（APIへのアクセス回数をへらすため）、`pprint`は辞書やリストをきれいに表示するため、`re`は正規表現に使用します。

```Python
# 標準ライブラリ
from functools import lru_cache
from pprint import pprint
import re
from xml.etree import ElementTree
# pip install requests
import requests
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux / Ubuntu |
| パッケージ管理 | pipenv |
| Python | version 3.8.5 |
| requests | 2.24.0 |

## 3. 法令番号の取得
法令の名前とは別に、「法令番号」という一意なIDが設定されているようです。番号とは言っても単純な連番ではなく、日本語の文字列です...

> 法令番号（ほうれいばんごう）とは、国家、地方自治体等により公布される各種の法令に対し、識別のため個別に付される番号をいう。一定の期間（暦年など）ごとに番号が初期化される（第1号から始まる）もの、ある特定の期日（独立記念日など）からの通し番号となっているもの等々、各政体によりその番号の管理、運用方法は異なる。
> 「法令番号」　出典: フリー百科事典『ウィキペディア（Wikipedia）』

法令本文を取得する際に法令番号を使って指定するため、名称から法令番号を検索する方法を確認します。

### 法令番号の辞書
法令名と法令番号の関係を辞書として取得する関数をまず作ります。

```Python:law_number.py
@lru_cache
def get_law_dict(category=1):
    # APIから各法令種別に含まれる法令リストを取得
    url = f"https://elaws.e-gov.go.jp/api/1/lawlists/{category}"
    r = requests.get(url)
    # XMLデータの解析
    root = ElementTree.fromstring(r.content.decode(encoding="utf-8"))
    # 辞書{名称: 法令番号}の作成
    names = [e.text for e in root.iter() if e.tag == "LawName"]
    numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
    return {name: num for (name, num) in zip(names, numbers)}
```

なお法令種別(`category`引数)は、4種類設定されています。

- 1: 全法令
- 2: 憲法、法律
- 3: 政令、勅令
- 4: 府省令

出力例：

```Python
pprint(get_law_dict(category=2), compact=True)
# ->
{
    "明治二十二年法律第三十四号（決闘罪ニ関スル件）": "明治二十二年法律第三十四号",
    "保管金規則": "明治二十三年法律第一号",
    "通貨及証券模造取締法": "明治二十八年法律第二十八号",
    "国債証券買入銷却法": "明治二十九年法律第五号",
    "民法": "明治二十九年法律第八十九号",
...
    "新型コロナウイルス感染症等の影響に対応するための国税関係法律の臨時特例に関する法律": "令和二年法律第二十五号",
    "令和二年度特別定額給付金等に係る差押禁止等に関する法律": "令和二年法律第二十七号",
    "防災重点農業用ため池に係る防災工事等の推進に関する特別措置法": "令和二年法律第五十六号"
}
```

「辞書{名称: 法令番号}の作成」の`root.iter()`はXMLデータをElement単位に分割してiterationとして返してくれます。なお`root.getiterator()`に置き換えても実行可能ですが、次の通り`DeprecationWarning`が発生するようです。

```
DeprecationWarning: This method will be removed in future versions.  Use 'tree.iter()' or 'list(tree.iter())' instead.
```

また各Elementには`.text`, `.tag`というタグが設定されています。`.tag`が`"LawName"`に一致するElementの`.text`は名称、`.tag`が`"LawNo"`に一致するElementの`.text`は法令番号を保存しているため、下記コードで名称と法令番号の辞書を作成しました。

```Python:get_law_dict() function
names = [e.text for e in root.iter() if e.tag == "LawName"]
numbers = [e.text for e in root.iter() if e.tag == "LawNo"]
return {name: num for (name, num) in zip(names, numbers)}
```

Elementのイメージ：

```Python:Elementのイメージ
elements = [
    (e.tag, e.text) for e in root.iter()
    if e.tag in set(["LawName", "LawNo"])
]
pprint(elements[:4], compact=False)
# ->
[('LawName', '歳入歳出予算概定順序'),
 ('LawNo', '明治二十二年閣令第十二号'),
 ('LawName', '予定経費算出概則'),
 ('LawNo', '明治二十二年閣令第十九号')]
```

### 名称のキーワード検索
法令の正式名を覚えている場合は少ないと思いますので、キーワード検索できるようにします。

```Python:law_number.py
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
```

出力例：

```Python:法令番号の取得
print(get_law_number("医薬品の臨床試験", category=4))
# ->
{
    '医薬品の臨床試験の実施の基準に関する省令': '平成九年厚生省令第二十八号',
    '動物用医薬品の臨床試験の実施の基準に関する省令': '平成九年農林水産省令第七十五号'
}
```

目的のJ-GCP(医薬品の臨床試験の実施の基準に関する省令)の法令番号が"平成九年厚生省令第二十八号"と判明しました。

## 4. 法令本文の取得
法令番号をAPIに送り、本文を取得します。XMLを解析して本文を取得して余計な空白や空行を削除します。

```Python:law_contents.py
@lru_cache
def get_raw(number):
    """
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
```

出力例：

```Python
gcp_raw = get_raw("平成九年厚生省令第二十八号")
pprint(gcp_raw, compact=False)
# ->
[
    "0",
    "平成九年厚生省令第二十八号",
...
    "目次",
...
    "第一章　総則",
    "（趣旨）",
    "第一条",
    "この省令は、被験者の人権の保護、安全の保持及び福祉の向上を図り、治験の科学的な質及び成績の信頼性を確保するため、医薬品、医療機器等の品質、有効性及び安全性の確保等に関する法律（以下「法」という。）第十四条第三項（同条第九項及び法第十九条の二第五項において準用する場合を含む。以下同じ。）並びに法第十四条の四第四項及び第十四条の六第四項（これらの規定を法第十九条の四において準用する場合を含む。以下同じ。）の厚生労働省令で定める基準のうち医薬品の臨床試験の実施に係るもの並びに法第八十条の二第一項、第四項及び第五項に規定する厚生労働省令で定める基準を定めるものとする。",
    "（定義）",
    "第二条",
...
    "附　則",
    "（施行期日）",
    "第一条",
    "この省令は、平成三十年四月一日から施行する。"
]
```


## 5. 本文の整形
句点で終わる行のみを取り出して結合します。また括弧内の文字列（例：「薬事法 **（昭和三十五年法律第百四十五号）**」）や「」を除去します。
さらにJ-GCPの場合は、第56条は言葉の読み替えに関する内容が主で解析には使用したくないため、除去しています。

```Python:law_contents.py
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
    # Remove article 56
    # contents = raw[:]
    contents = raw[: raw.index("第五十六条")]
    # Select sentenses
    contents = [s for s in contents if s.endswith("。")]
    # Join the sentenses
    gcp = "".join(contents)
    # 「 and 」 will be removed
    gcp = gcp.translate(str.maketrans({"「": "", "」": ""}))
    #　Strings enclosed with （ and ） will be removed
    return re.sub("（[^（|^）]*）", "", gcp)
```

出力例：

```Python:J-GCPの整形
gcp = preprocess_gcp(gcp_raw)
# ->
"""薬事法第十四条第三項、第十四条の四第四項並びに第十四条の五第四項、
第八十条の二第一項、第四項及び第五項並びに第八十二条の規定に基づき、
医薬品の臨床試験の実施の基準に関する省令を次のように定める。
この省令は、被験者の人権の保護、安全の保持及び福祉の向上を図り、
治験の科学的な質及び成績の信頼性を確保するため、医薬品、医療機器等の品質、
有効性及び安全性の確保等に関する法律...
当該治験への参加について文書により同意を得なければならない。"""
```

第56条を削除する部分については、他の法令の場合は`contents = raw[:]`などに置き換えてください。

### 6. まとめ
クラスにまとめました。

```Python:law_all.py
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
```

使い方：

```Python:LawLoaderの使い方
# The Constitution of Japan
loader2 = LawLoader(category=2)
consti_number = loader2.get_law_number("日本国憲法")
print(consti_number)
consti_raw = loader2.get_raw("昭和二十一年憲法")
consti = loader2.pre_process(consti_raw)
# J-GCP：データ整形を含めてメソッドとして登録済
loader4 = LawLoader(category=4)
gcp = loader4.gcp()
```

## 7. あとがき
自然言語処理の題材として、日本の法令をダウンロードして整形しました。

お疲れさまでした！
