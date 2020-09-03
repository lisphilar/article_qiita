# [Python] 自然数を序数に変換する

## Contents
integer型の自然数をstring型の序数（0th, 1st, 2nd, 3rd,..）に変換する方法です。ここでは0も自然数に含みます。

## Rule
実装の前に、[英語の序数1から1000までの表記と読み方一覧](https://kw-note.com/translation/english-ordinal-numbers/)を参考にしてルールをまず考えます。

1. 序数のsuffix (数字に続く文字列)は基本的に"th"です！（おおざっぱ）
2. 例外として、下1桁が1の場合は"st", 2の場合は"nd", 3の場合は"rd"となります。
3. さらに例外ルールに対する例外として、下2桁が11の場合は"th"になります（eleventh）。

## 解決方法
上記ルールを順番にコーディングしてみます。

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux |
| Python | version 3.8.5 |

### 1.基本的に"th"
collectionsパッケージの`defaultdict`を使用すると[^1]、

[^1]: [Python defaultdict の使い方](https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7)

```Python
from collections import defaultdict
ordinal_dict = defaultdict(lambda: "th")
# 見境なく"th"を返す
print(ordinal_dict[0])
# -> 'th'
print(ordinal_dict[1])
# -> 'th': ルール2で修正
print(ordinal_dict[11])
# -> 'th': ルール3で修正
```

### 2. 下1桁が1の場合は"st", 2の場合は"nd", 3の場合は"rd"
辞書を更新します。

```Python
ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
print(ordinal_dict[0])
# -> 'th'
print(ordinal_dict[1])
# -> 'st'
print(ordinal_dict[11])
# -> 'th': ルール3で修正
```

### 3. 下2桁が11の場合は"th"
