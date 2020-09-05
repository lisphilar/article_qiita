# [Python] 自然数を序数に変換する

## Contents
integer型の自然数をstring型の序数（0th, 1st, 2nd, 3rd,..）に変換する方法です。ここでは0も自然数に含みます。
各コードは[GitHub repository](https://github.com/lisphilar/article_qiita/tree/master/python/02_n-th_string)からダウンロードできます。

## Rule
実装の前に、[英語の序数1から1000までの表記と読み方一覧](https://kw-note.com/translation/english-ordinal-numbers/)を参考にしてルールをまず考えます。

1. 序数のsuffix (数字に続く文字列)は基本的に"th"です！（おおざっぱ）
2. 例外として、下1桁が1の場合は"st", 2の場合は"nd", 3の場合は"rd"となります。
3. さらに例外ルールに対する例外として、下2桁が11の場合は"th"になります（eleventh）。

## 解決方法
上記ルールを順番にコーディングし、最後にリファクタリング（挙動を変えずにコードを整理）します。

使用するパッケージ：

```Python
# 標準ライブラリ
from collections import defaultdict
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux |
| Python | version 3.8.5 |


### 1.基本的に"th"
collectionsパッケージの`defaultdict`を使用すると[^1]、

[^1]: [Python defaultdict の使い方](https://qiita.com/xza/items/72a1b07fcf64d1f4bdb7)

```Python
def int2ordinal_1(num):
    ordinal_dict = defaultdict(lambda: "th")
    suffix = ordinal_dict[num]
    return f"{num}{suffix}"

# 見境なく"th"を返す
print(int2ordinal_1(0))
# -> '0th'
print(int2ordinal_1(1))
# -> '1th': ルール2で対応, 正しくは1st'
print(int2ordinal_1(11))
# -> '11th': ルール3で対応
```

### 2. 下1桁が1の場合は"st", 2の場合は"nd", 3の場合は"rd"
辞書を更新します。

```Python
ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
```

そして、入力値の下1桁に基づいて序数を判断するように変更します。

```Python
mod = num % 10
suffix = ordinal_dict[mod]
```

これを関数内の処理に加えると、

```Python
def int2ordinal_2(num):
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    mod = num % 10
    suffix = ordinal_dict[mod]
    return f"{num}{suffix}"

print(int2ordinal_2(0))
# -> '0th'
print(int2ordinal_2(1))
# -> '1st'
print(int2ordinal_2(11))
# -> '11st': ルール3で対応, 正しくは11th'
```

### 3. 下2桁が11の場合は"th"
100で割ったあまりが11のときに"th"を返せばよいので、

```Python
if num % 100 == 11:
    suffix = "th"
else:
    suffix = ordinal_dict[mod]
```

これを関数内の処理に加えると、

```Python
def int2ordinal_3(num):
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    mod = num % 10
    if num % 100 == 11:
        suffix = "th"
    else:
        suffix = ordinal_dict[mod]
    return f"{num}{suffix}"

print(int2ordinal_3(0))
# -> '0th'
print(int2ordinal_3(1))
# -> '1st'
print(int2ordinal_3(11))
# -> '11th'
```

### 4. リファクタリング
時間のかかる処理ではないので、あくまでおまけです。

`num % 100 == 11`は「商`num // 10`を10で割ったときの余りが1」と同じですね。

```Python
# 変更前
mod = num % 10
if num % 100 == 11:
    suffix = "th"
else:
    suffix = ordinal_dict[mod]
# 変更後
q = num // 10
mod = num % 10
if q % 10 == 1:
    suffix = "th"
else:
    suffix = ordinal_dict[mod]
```

さらに、商と余りは`divmod`関数で一度に求められます。

また、if-else文を1行にします。今回は効果が薄いですが、代数`suffix`を書く回数が減るので誤記を減らせます。

```Python
q, mod = divmod(num, 10)
suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
```

これを関数内の処理に加えると、

```Python
def int2ordinal_4(num):
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    q, mod = divmod(num, 10)
    suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
    return f"{num}{suffix}"

print(int2ordinal_4(0))
# -> '0th'
print(int2ordinal_4(1))
# -> '1st'
print(int2ordinal_4(11))
# -> '11th'
```

## 完成形：序数を返す関数
引数の型チェックなどを加えると下記の通りです。

```Python:ordinal_func.py
def int2ordinal(num):
    """
    Convert a natural number to a ordinal number.

    Args:
        num (int): natural number

    Returns:
        str: ordinal number, like 0th, 1st, 2nd,...

    Notes:
        Zero can be used as @num argument.
    """
    if not isinstance(num, int):
        raise TypeError(
            f"@num must be integer, but {num} was applied.")
    if num < 0:
        raise ValueError(
            f"@num must be over 0, but {num} was applied.")
    ordinal_dict = defaultdict(lambda: "th")
    ordinal_dict.update({1: "st", 2: "nd", 3: "rd"})
    q, mod = divmod(num, 10)
    suffix = "th" if q % 10 == 1 else ordinal_dict[mod]
    return f"{num}{suffix}"
```

実行確認：

```Python:ordinal_func.py
print(int2ordinal(0)) # 0th
print(int2ordinal(1)) # 1st
print(int2ordinal(2)) # 2nd
print(int2ordinal(3)) # 3rd
print(int2ordinal(4)) # 4th
print(int2ordinal(11)) # 11th
print(int2ordinal(21)) # 21st
print(int2ordinal(111)) # 111th
print(int2ordinal(121)) # 121st
```

## 別解（defaultdictを使わない方法）
@shiracamusさんよりコメントいただいた、`defaultdict`を使わない方法をご紹介します。

```Python
def int2ordinal_5(num):
    ordinal_dict = {1: "st", 2: "nd", 3: "rd"}
    q, mod = divmod(num, 10)
    suffix = q % 10 != 1 and ordinal_dict.get(mod) or "th"
    return f"{num}{suffix}"

print(int2ordinal_5(0))
# -> '0th'
print(int2ordinal_5(1))
# -> '1st'
print(int2ordinal_5(11))
# -> '11th'
```

|num|q|mod|q % 10 != 1|ordinal_dict.get(mod)|q % 10 != 1 and ordinal_dict.get(mod)|suffix|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|0|0|0|False|None|False|"th"|
|1|0|1|True|"st"|"st"|"st"|
|11|1|1|False|"st"|False|"th"|

否定形と`and`を組み合わせるとは...

ここまではなかなか思いつかないとは思いますが、`or`を数値代入に使用する方法は便利です。たとえば、関数について引数のデフォルト値を空のリストを与えたいときに使えます。（関数の引数に`def func(x=[]): x.append(0); return x`などと設定すると想定外の挙動を示すので注意！[^2]）

[^2]: [【python】引数のデフォルト値は定義時評価なので注意](https://www.haya-programming.com/entry/2018/11/06/015506)

```Python
def func(values=None):
    values = values or []
    if not isinstance(values, list):
        raise TypeError(f"@values must be a list or None, but {values} was applied.")
    values.append(0)
    return values
```

`values`がNoneやFalse, 空であったときは空のリスト`[]`が代入されます。それ以外のときは`values`引数がそのまま使用されます。

## あとがき
以上、Pythonで自然数を序数に変換する方法でした！
