# [CovsirPhy] COVID-19データ解析用Pythonパッケージ: Phase setting

## Introduction

COVID-19のデータ（PCR陽性者数など）のデータを簡単にダウンロードして解析できるPythonパッケージ [CovsirPhy](https://github.com/lisphilar/covid19-sir)を作成しています。

紹介記事：

- [SIR model](https://qiita.com/Lisphilar/items/ac5a5fda02d8359d6a94)
- [SIR-F model](https://qiita.com/Lisphilar/items/99c1e7673bc13d77dfcc)
- [Data loading](https://qiita.com/Lisphilar/items/34337bd89ad485ec4a4b)
- [S-R trend analysis](https://qiita.com/Lisphilar/items/a0754e978172f20f6c4a)
- [Parameter estimation](https://qiita.com/Lisphilar/items/bf0f2af9f0c688e23cd9)

**今回はPhase setting（ODE modelのパラメータが一定となる期間ごとに分割する方法）のご紹介です。**

英語版のドキュメントは[CovsirPhy: COVID-19 analysis with phase-dependent SIRs](https://lisphilar.github.io/covid19-sir/index.html), [Kaggle: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model)をご参照ください。

## 1. 実行環境
CovsirPhyは下記方法でインストールできます！Python 3.7以上, もしくはGoogle Colaboratoryをご使用ください。

- 安定版：`pip install covsirphy --upgrade`
- 開発版：`pip install "git+https://github.com/lisphilar/covid19-sir.git#egg=covsirphy"`

```Python
import covsirphy as cs
cs.__version__
# '2.8.2'
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux / Ubuntu |
| Python | version 3.8.5 |

## 2. 準備
実データを[COVID-19 Data Hub](https://covid19datahub.io/)[^1]よりダウンロードするコード[^2]はこちら：

[^1]: Guidotti, E., Ardia, D., (2020), “COVID-19 Data Hub”, Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.
[^2]: [[CovsirPhy] COVID-19データ解析用Pythonパッケージ: Data loading](https://qiita.com/Lisphilar/items/34337bd89ad485ec4a4b)

```Python
data_loader = cs.DataLoader("input")
jhu_data = data_loader.jhu()
population_data = data_loader.population()
```

本記事の表及びグラフでは、下記コード[^3]により2020/9/17時点の日本のデータ（厚生労働省発表の全国の合計値）を用いています。[COVID-19 Data Hub](https://covid19datahub.io/)[^1]にも日本のデータが含まれますが、厚生労働省発表の全国の合計値とは異なるようです。

[^3]: [[CovsirPhy] COVID-19データ解析用Pythonパッケージ: S-R trend analysis](https://qiita.com/Lisphilar/items/a0754e978172f20f6c4a)

```Python
# (Optional) 厚生労働省データの取得
# エラーが出る場合は"pip install requests aiohttp"
japan_data = data_loader.japan()
jhu_data.replace(japan_data)
print(japan_data.citation)
```

実データの確認：

```Python
# 解析用クラスのインスタンス生成
snl = cs.Scenario(jhu_data, population_data, country="Japan")
# 実データの確認
snl.records(filename=None)
```

実データのグラフ：



## 3. scenarioとは
Covsirphyの`Scenario`クラスでは、Phase[^3]の設定内容を複数種類登録することができます。「Phase[^3]の設定内容」を"scenario"と呼んでおり、内部的には`PhaseSeries`クラスが担当しています（クラス名と名称がずれてしまってすみません...`Scenario`クラスを実装したあとで`PhaseSeries`クラスを作成した結果、こうなりました）。

たとえば次の表のように"Scenario A", "Scenario B", "Scenario C"を並列して設定し、シナリオ分析を実行することができます。2020/2/6から2020/9/17までの実データが得られている、という前提で日付を記載しています。

|scenario名|0th|1st|2nd|3rd|
|:--:|:--:|:--:|:--:|:--:|
|scenario A|2/6 - 6/30|7/1 - 9/17|9/18 - 12/31|(該当なし)|
|scenario B|2/6 - 8/31|9/1 - 9/17|9/18 - 12/31|(該当なし)|
|scenario C|2/6 - 8/31|9/1 - 9/17|9/18 - 10/31|11/1 - 12/31|

scenario A, B, Cそれぞれについて0th/1st/2nd phaseのパラメータ推定を行い、1st phaseのパラメータを使って2nd phaseの患者数をシュミレーションし、scenario Cについては2ndから3rdの間に$\rho$が半減すると仮定してシュミレーションを実行すれば、

- Phase設定を最適化したいとき：AとBのパラメータ推定についてRMSLEを比較すればOK
- 10/1に$\rho$が半減した場合の患者数への効果を検討したいとき：BとCの11/1kら12/1の間の患者数推移を比較すればOK

## 4. シナリオの作成/初期化/削除
シナリオ自体の作成/初期化/削除方法は次の通りです。デフォルトのシナリオ"Main"とそのほかのシナリオに分けてご説明います。

### Main scenario
`Scenario.trend()`や`Scenario.estimate()`メソッドにおいて"name"引数を指定しない場合はデフォルトのシナリオ名"Main"が自動的に使用されます。作成は不要、削除は不可となっています。

```Python
# 初期化（実データの最終日の翌日以降のPhaseを削除する）
snl.clear()
# 初期化（実データの最終日以前を含めてすべてのPhaseを削除する）
snl.clear(include_past=True)
```

### Another scenario
"name"引数を指定すると任意のシナリオ名を使用することができます。ここでは例として"Another"シナリオを作成、初期化、削除します。なお作成時には、Main scenarioの設定がそのままコピーされます（編集方法は後述）。

```Python
# 作成（Main scenarioの設定がコピーされる）
snl.clear(name="Another")
# 初期化（実データの最終日の翌日以降のPhaseを削除する）
Scenario.clear(name="Another")
# 初期化（実データの最終日以前を含めてすべてのPhaseを削除する）
Scenario.clear(name="Another", include_past=True)
# 削除
Scenario.delete(name="Another")
```

## 5. シナリオの一覧表示
`Scenario.summary()`メソッドによりシナリオの情報を`pandas.DataFrame`形式で一覧表示できます。表示する情報の種類（一覧の列名）を指定したり、特定のシナリオのみ表示することも可能です。

```Python
# すべて表示：
# Main scenarioのみ登録されている場合、indexはphase (0th, 1st,..)
# Main以外も登録されている場合、indexはシナリオ名とphase
snl.summary()
# 列名を指定
snl.summary(columns=["Start", "End"])
# 特定のシナリオのみ表示
snl.summary(name="Main")
```

なお`Scenario.trend()`, `Scenario.add()`などのメソッドは`self`を返すため、`Scenario.trend().summary()`などとPhaseの編集と一覧表示をコマンド1行でまとめて実行できます。

## 6. S-R trend analysisによるphase設定
S-R trend analysis[^3]により自動的にphaseを設定できます。

```Python
snl.trend(filename=None).summary()
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 04Jul2020 |    126529100 |
| 2nd | Past   | 05Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 05Sep2020 |    126529100 |
| 7th | Past   | 06Sep2020 | 17Sep2020 |    126529100 |

## 7. Future phaseの追加
