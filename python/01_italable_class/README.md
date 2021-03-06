## Contents
Pythonのクラスで反復処理[^1]を行う方法の解説記事です。
各コードは[GitHub repository](https://github.com/lisphilar/article_qiita/tree/master/python/01_italable_class)からダウンロードできます。

[^1]: [Qiita: Pythonのfor文〜iterableってなに〜](https://qiita.com/conf8o/items/7ee98d103e94caa8b5dd)

```Python:iter_minimum.py
iteration = IterClass(["a", "ab", "abc", "bb", "cc"])
print([v for v in iteration if "a" in v])
# ['a', 'ab', 'abc']
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux |
| Python | version 3.8.5 |

## 解決方法
クラスの特殊メソッド`__iter__`[^2]と`yield from`構文[^3]によって実装できます。リストまたはタプルを記憶し、繰り返し処理として呼び出された際に先頭から順番に返します。

[^2]: [Life with Python: Python のイテレータ生成クラスの使い方](https://www.lifewithpython.com/2015/11/python-create-iterator-protocol-class.html)
[^3]: [blanktar: python3.3のyield fromとは何なのか](https://blanktar.jp/blog/2015/07/python-yield-from)

```Python:iter_minimum.py
class IterClass(object):
    """
    Iterable class.

    Args:
        values (list[object] or tuple(object)): list of values

    Raises:
        TypeError: @values is not a list/tuple
    """

    def __init__(self, values):
        if not isinstance(values, (list, tuple)):
            raise TypeError("@values must be a list or tuple.")
        self._values = values

    def __iter__(self):
        yield from self._values
```


## 応用（`__bool__`との組み合わせ）
上記の例では新しいクラスを作成する意義が感じられないので、応用バージョンを作りました。

### 最小単位の作成
反復処理で返される最小単位`Unit`クラスをまず作成します。

```Python:iter_advanced.py
class Unit(object):
    """
    The smallest unit.
    """

    def __init__(self, value):
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"@value must be integer or float value, but {value} was applied.")
        self._value = value
        self._enabled = True

    def __bool__(self):
        return self._enabled

    @property
    def value(self):
        """
        float: value of the unit
        """
        return self._value

    def enable(self):
        """
        Enable the unit.
        """
        self._enabled = True

    def disable(self):
        """
        Disable the unit.
        """
        self._enabled = False
```

`Unit`は固有の値と状態（`__bool__`: True/False）を持っています。

Unitの作成：

```Python:iter_advanced.py
unit1 = Unit(value=1.0)
# Unitの状態がTrueであれば値を表示
if unit1:
    print(unit1.value)
# 1.0
```

状態をFalseに：

```Python:iter_advanced.py
# Disable
unit1.disable()
# Unitの状態がTrueであれば値を表示
if unit1:
    print(unit1.value)
# 出力なし
```

状態をTrueに：

```Python:iter_advanced.py
# Disable
unit1.enable()
# Unitの状態がTrueであれば値を表示
if unit1:
    print(unit1.value)
# 1.0
```

### 反復処理を行うクラス
複数の`Unit`の情報を保管して反復処理を行うクラス`Series`を作成します。

```Python:iter_advanced.py
class Series(object):
    """
    A series of units.
    """

    def __init__(self):
        self._units = []

    def __iter__(self):
        yield from self._units

    def add(self, unit):
        """
        Append a unit.

        Args:
            unit (Unit]): the smallest unit

        Raises:
            TypeError: unit is not an instance of Unit
        """
        if not isinstance(unit, Unit):
            raise TypeError("@unit must be a instance of Unit")
        self._units.append(unit)

    def _validate_index(self, num):
        """
        Validate the index number.

        Args:
            num (int): index number of a unit

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        if not isinstance(num, int):
            raise TypeError(
                f"@num must be integer, but {num} was applied.")
        try:
            self._units[num]
        except IndexError:
            raise IndexError(f"@num must be under {len(self._units)}")

    def enable(self, num):
        """
        Enable a unit.

        Args:
            num (int): index of the unit to be enabled

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        self._validate_index(num)
        self._units[num].enable()

    def disable(self, num):
        """
        Disable a unit.

        Args:
            num (int): index of the unit to be disabled

        Raises:
            TypeError: @num is not an integer
            IndexError: @num is not a valid index number
        """
        self._validate_index(num)
        self._units[num].disable()
```

### 状態がTrueとなっているUnitの値を返す関数
`Series`クラスの挙動を確認するため、状態がTrueとなっているUnitの値を返す関数を作ります。

```Python:iter_advanced.py
def show_enabled(series):
    """
    Show the values of enabled units.
    """
    if not isinstance(series, Series):
        raise TypeError("@unit must be a instance of Series")
    print([unit.value for unit in series if unit])
```

### 挙動確認
`Unit`を`Series`に登録し、すべての`Unit`の値を表示します。

```Python:iter_advanced.py
# Create a series of units
series = Series()
[series.add(Unit(i)) for i in range(6)]
show_enabled(series)
# [0, 1, 2, 3, 4, 5]
```

5, 6番目のUnit（値は4, 5）の状態をFalseにすると...

```Python:iter_advanced.py
# Disable two units
series.disable(4)
series.disable(5)
show_enabled(series)
# [0, 1, 2, 3]
```

5番目のUnit（値は4）の状態をTrueに戻すと...

```Python:iter_advanced.py
# Enable one disabled unit
series.enable(4)
show_enabled(series)
# [0, 1, 2, 3, 4]
```

## あとがき
閲覧ありがとうございます。お疲れ様でした。

この記事を作成したきっかけ：
自作のPython package [CovsirPhy: COVID-19 analysis with phase-dependent SIRs](https://github.com/lisphilar/covid19-sir)でこの仕組みを使いました。
- [PhaseUnit: ODEモデルのパラメータ値が一定となる期間](https://github.com/lisphilar/covid19-sir/blob/master/covsirphy/phase/phase_unit.py)
- [PhaseSeries: 感染者数のシナリオ](https://github.com/lisphilar/covid19-sir/blob/master/covsirphy/phase/phase_series.py)
