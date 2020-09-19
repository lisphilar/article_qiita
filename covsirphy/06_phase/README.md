# [CovsirPhy] COVID-19データ解析用Pythonパッケージ: Phase設定の最適化

## Introduction

COVID-19のデータ（PCR陽性者数など）のデータを簡単にダウンロードして解析できる拙作のPythonパッケージ [CovsirPhy](https://github.com/lisphilar/covid19-sir)の紹介記事です。

1. [SIR model](https://qiita.com/Lisphilar/items/ac5a5fda02d8359d6a94)
2. [SIR-F model](https://qiita.com/Lisphilar/items/99c1e7673bc13d77dfcc)
3. [Data loading](https://qiita.com/Lisphilar/items/34337bd89ad485ec4a4b)
4. [S-R trend analysis](https://qiita.com/Lisphilar/items/a0754e978172f20f6c4a)
5. [Parameter estimation](https://qiita.com/Lisphilar/items/bf0f2af9f0c688e23cd9)

**今回はPhase設定の最適化方法についてご説明します。**

英語版のドキュメントは[CovsirPhy: COVID-19 analysis with phase-dependent SIRs](https://lisphilar.github.io/covid19-sir/index.html), [Kaggle: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model)をご参照ください。

## 1. 実行環境
CovsirPhyは下記方法でインストールできます！Python 3.7以上, もしくはGoogle Colaboratoryをご使用ください。

- 安定版：`pip install covsirphy --upgrade`
- 開発版：`pip install "git+https://github.com/lisphilar/covid19-sir.git#egg=covsirphy"`

```Python
import covsirphy as cs
cs.__version__
# '2.8.3'
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

本記事の表及びグラフでは、下記コード[^3]により2020/9/19時点の日本のデータ（厚生労働省発表の全国の合計値）を用いています。[COVID-19 Data Hub](https://covid19datahub.io/)[^1]にも日本のデータが含まれますが、厚生労働省発表の全国の合計値とは異なるようです。

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
# 実データのグラフ表示
snl.records(filename=None)
```

## 3. scenarioとは
Covsirphyの`Scenario`クラスでは、Phase[^3]の設定内容を複数種類登録することができます。「Phase[^3]の設定内容」を"scenario"と呼んでおり、内部的には`PhaseSeries`クラスが担当しています（クラス名と名称がずれてしまってすみません...`Scenario`クラスを実装したあとで`PhaseSeries`クラスを作成した結果、こうなりました）。

たとえば次の表のように"Scenario A", "Scenario B", "Scenario C"を並列して設定し、シナリオ分析を実行することができます。2020/2/6から2020/9/19までの実データが得られている、という前提で日付を記載しています。

|scenario名|0th|1st|2nd|3rd|
|:--:|:--:|:--:|:--:|:--:|
|scenario A|2/6 - 6/30|7/1 - 9/19|9/20 - 12/31|(該当なし)|
|scenario B|2/6 - 8/31|9/1 - 9/19|9/20 - 12/31|(該当なし)|
|scenario C|2/6 - 8/31|9/1 - 9/19|9/20 - 10/31|11/1 - 12/31|

scenario A, B, Cそれぞれについて0th/1st/2nd phaseのパラメータ推定を行い、1st phaseと2nd phaseのパラメータは同一、scenario Cについては2ndから3rdの間に$\rho$が半減すると仮定して患者数のシュミレーションを実行すれば、

- **Phase設定を最適化したいとき：AとBのパラメータ推定についてRMSLEを比較すればOK**
- 11/1に$\rho$が半減した場合の患者数への効果を検討したいとき：BとCの11/1ら12/1の間の患者数推移を比較すればOK

本記事では「Phase設定を最適化したいとき」に焦点を当てます。

## 4. シナリオの作成/初期化/削除
シナリオ自体の作成/初期化/削除方法は次の通りです。デフォルトのシナリオ"Main"とそのほかのシナリオに分けてご説明します。

### Main scenario
`Scenario.trend()`や`Scenario.estimate()`メソッドにおいて"name"引数を指定しない場合はデフォルトのシナリオ名"Main"が自動的に使用されます。作成は不要、削除は不可となっています。

```Python
# 初期化（実データの最終日の翌日以降のPhaseを削除する）
snl.clear()
# 初期化（実データの最終日以前を含めてすべてのPhaseを削除する）
snl.clear(include_past=True)
# パラメータ推定
snl.estimate(cs.SIRF)
```

### Another scenario
"name"引数を指定すると任意のシナリオ名を使用することができます。ここでは例として"Another"シナリオを作成、初期化、削除します。なお作成時には、Main scenarioの設定がそのままコピーされます（編集方法は後述）。

```Python
# 作成（Main scenarioの設定をコピーする）
# @templateのデフォルト値：Main
snl.clear(name="Another", template="Main")
# 初期化（実データの最終日の翌日以降のPhaseを削除する）
Scenario.clear(name="Another")
# 初期化（実データの最終日以前を含めてすべてのPhaseを削除する）
Scenario.clear(name="Another", include_past=True)
# パラメータ推定
snl.estimate(cs.SIRF, name="Another")
# 削除
Scenario.delete(name="Another")
```

## 5. シナリオの一覧表示
`Scenario.summary()`メソッドによりシナリオの情報を`pandas.DataFrame`形式で一覧表示できます。表示する情報の種類（一覧の列名）を指定したり、特定のシナリオのみ表示したりことも可能です。

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
以降の章ではphase設定の編集方法を順にご説明します。

まず、S-R trend analysis[^3]により自動的にphaseを設定できます。

```Python
# Main: S-R trend analysis
snl.trend(filename=None).summary()
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 7th | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

## 7. phaseの無効化と有効化
phaseの期間は変えたくないが、特定のphaseについてはパラメータ推定などをスキップしたい場合、`Scenario.disable(phases)`を使用して当該ののphaseを無効化できます。引数が"phases"と複数形になっていることに注意してください。リストを与える必要があります。

```Python
# MainをコピーしてScenario Aを作成する
snl.clear(name="A")
# A: 0th phaseと3rd phaseを無効化する
snl.disable(phases=["0th", "3rd"], name="A").summary(name="A")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 7th | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

一覧から0th/3rd phaseの行がなくなっていますが、他のphaseの開始日や終了日は変更されていません。

また無効化されたphaseは`Scenario.enable(phases)`によって有効化できます。

```Python
# A: 0th phaseを再有効化する
snl.enable(phases=["0th"], name="A").summary(name="A")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 7th | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

0th phaseが一覧に表示されました。3rd phaseは無効化されたままです。

## 7. phaseの結合
phaseを結合したい場合は`Scenario.combine(phases=[最初のphase名, 最後のphase名])`をご使用ください。

```Python
# MainをコピーしてScenario Bを作成する
snl.clear(name="B")
# B: 1st phase から5th phaseまでを1つのphaseにまとめる
snl.combine(phases=["1st", "5th"], name="B")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 28Aug2020 |    126529100 |
| 2nd | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 3rd | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

- 実行前：1st phase (22Apr2020 - 06Jul2020),..., 5th phase (15Aug2020 - 28Aug2020)
- 実行後：1st phase (22Apr2020 - 28Aug2020)

2nd/3rd/4th/5th phaseに所属する日付がなくなったため、6th/7th phaseの名称が2nd/3rdに変更されています。

## 8. phaseの削除
特定のphaseを削除できますが、phaseの位置によって各日付の新規所属先が異なります。

### [削除] 0th phaseの場合
0th phaseは削除できず、`Scenario.delete(phase=["0th"])`としても0th phaseが無効化されるのみで1st phaseの開始日は変わりません。

```Python
# MainをコピーしてScenario Cを作成する
snl.clear(name="C")
# C: 0th phaseと3rd phaseを無効化する
snl.delete(phases=["0th"], name="C").summary(name="C")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 7th | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

結果は省略しますが、`Scenario.enable(phases=["0th"])`により再有効化できます。

### [削除] 途中のphaseの場合
0th phaseでもなく、最後尾のphase (今回は7th phase)も含まれない場合、対象のphaseは一つ前のphaseに吸収されます。`Scenario.combine()`と同じです。

```Python
# MainをコピーしてScenario Dを作成する
snl.clear(name="D")
# D: 3rd phaseを削除して2nd phaseに吸収させる
snl.delete(phases=["3rd"], name="D").summary(name="D")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 01Aug2020 |    126529100 |
| 3rd | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 4th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 5th | Past   | 29Aug2020 | 08Sep2020 |    126529100 |
| 6th | Past   | 09Sep2020 | 19Sep2020 |    126529100 |

- 実行前：2nd phase (07Jul2020 - 23Jul2020), 3rd phase (24Jul2020 - 01Aug2020)
- 実行後：2nd phase (07Jul2020 - 01Aug2020)

また、3rd phaseが空になったので4th/5th/6th/7thが3rd/4th/5th/6thにスライドしています。


### [削除] 後続phaseがない場合
7th phaseのみ、あるいは6th phaseと7th phaseの両方を削除する場合など後続のphaseがない場合は、6th/7th phaseに所属していた日付はどのphaseにも所属しない状態になります。

```Python
# MainをコピーしてScenario Eを作成する
snl.clear(name="E")
# E: 6th/7th phaseを削除し、29Aug2020以降の所属を破棄
snl.delete(phases=["last"], name="E").summary(name="E")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |

6th/7th phaseに所属していた29Aug2020 - 19Sep2020が一覧に表示されなくなりました。


## 9. phaseの追加
`Scenario.add()`を使って後続のphaseを追加します。29Aug2020以降がどのphaseにも所属していないScenario Eを例とします。

### [追加] 最終日を指定
`Scenario.add(end_date="31Aug2020")`のように最終日を指定して新しいphaseを追加できます。

```Python
# E: 31Aug2020までを6th phaseとして追加
snl.add(end_date="31Aug2020", name="E").summary(name="E")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 31Aug2020 |    126529100 |

### [追加] 日数を指定
`Scenario.add(days=10)`のように日数を指定して新しいphaseを追加できます。

```Python
# E: 01Sep2020 (6th最終日の翌日)から10日間を7thとして追加
snl.add(days=10, name="E").summary(name="E")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 31Aug2020 |    126529100 |
| 7th | Past   | 01Sep2020 | 10Sep2020 |    126529100 |

### [追加] データの最終日まで
`Scenario.add()`について終了日及び日数を指定しない場合は、データの最終日（今回は19Sep2020）までを1つのphase新しいphaseを追加できます。

```Python
# E: 11Sep2020 (7th最終日の翌日)から19Sep2020までを8thとして追加
snl.add(days=10, name="E").summary(name="E")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 2nd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 6th | Past   | 29Aug2020 | 31Aug2020 |    126529100 |
| 7th | Past   | 01Sep2020 | 10Sep2020 |    126529100 |
| 8th | Past   | 11Sep2020 | 19Sep2020 |    126529100 |

## 10. phaseの分割
`Scenario.separate(date)`により、phaseを分割することができます。指定した日付が分割後の2つ目のphaseの開始日となります。9章で使用したScenario Eの0th phase (06Feb2020 - 21Apr2020)を(06Feb2020 - 31Mar2020), (01Apr2020 - 21Apr2020)に分割するコードはこちらです。

```Python
# Scenario EをコピーしてScenario Fを作成する
snl.clear(name="F", template="E")
# E: 01Apr2020を1st phaseの開始日として0th phaseを分割する
snl.separate(date="01Apr2020", name="F").summary(name="F")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 31Mar2020 |    126529100 |
| 1st | Past   | 01Apr2020 | 21Apr2020 |    126529100 |
| 2nd | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 3rd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 4th | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 5th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 6th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 7th | Past   | 29Aug2020 | 31Aug2020 |    126529100 |
| 8th | Past   | 01Sep2020 | 10Sep2020 |    126529100 |
| 9th | Past   | 11Sep2020 | 19Sep2020 |    126529100 |

0th phaseの最終日が31Mar2020, 1st phaseの開始日が01Apr2020になりました。後続の1st phase以降は2nd phase以降にスライドしています。

## 11. Phase設定の最適化
まとめとしてPhase設定の最適化、つまりパラメータ推定の正確性が高まるようにPhaseの区切りを最適化する方法についてご説明します。0th phaseと1st phaseの境界を最適化したい場合、手順は次の通りです。

a. 区切りの候補日を挙げる
b. 候補となる日付が1st phaseの開始日となるように区切りを変更する
c. 0th/1st phaseについてパラメータ推定を行い、RMSLEを計算する
d. RMSLEを比較し、より低い値を示した候補日を選択する

### 区切りの変更
実装に移る前に、区切りを変更する方法についてご説明します。

`Scenario.combine()`及び`Scenario.separate()`を組み合わせれば、phaseの区切りを変更することができます。例として、10章で使用したScenario Fを使用します。

変更前：0th phase (06Feb2020 - 31Mar2020), 1st phase (01Apr2020 - 21Apr2020)
変更後：0th phase (06Feb2020 - 11Apr2020), 1st phase (12Apr2020 - 21Apr2020)

```Python
# Scenario FをコピーしてScenario Gを作成する
snl.clear(name="G", template="F")
# G: 0th phaseと1st phaseを結合する
snl.combine(phases=["0th", "1st"], name="G")
# G: 12Apr2020を1st phaseの開始日として0th phaseを分割する
snl.separate(date="12Apr2020", name="G").summary(name="G")
```

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 11Apr2020 |    126529100 |
| 1st | Past   | 12Apr2020 | 21Apr2020 |    126529100 |
| 2nd | Past   | 22Apr2020 | 06Jul2020 |    126529100 |
| 3rd | Past   | 07Jul2020 | 23Jul2020 |    126529100 |
| 4th | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 5th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 6th | Past   | 15Aug2020 | 28Aug2020 |    126529100 |
| 7th | Past   | 29Aug2020 | 31Aug2020 |    126529100 |
| 8th | Past   | 01Sep2020 | 10Sep2020 |    126529100 |
| 9th | Past   | 11Sep2020 | 19Sep2020 |    126529100 |

### 実装
Phase設定の最適化の実装方法です。まず、候補日の設定と最適化用インスタンスの作成を行います。

区切りの候補日は0th phaseの3日目から1st phaseの終了日3日前となります。Phaseの期間が3日以内になるとパラメータ推定が難しくなります。今回は例として、候補日は01Mar2020と12Apr2020のみに絞って話を進めます。

```Python
# 候補日
candidates = ["01Mar2020", "12Apr2020"]
# RMSLEの登録用dictionary
opt_dict = {date: {} for date in candidates}
# 最適化用インスタンス：(Optional) tau valueを揃える
snl_opt = cs.Scenario(jhu_data, population_data, country="Japan", tau=720)
# S-R trend analysis
snl_opt.trend(show_figure=False)
```

候補日ごとに、シナリオを作成し、区切りの変更、パラメータ推定、RMSLEの記録を行います。`Scenario.estimate()`の"phases"引数と"name"引数を設定すると、目的のシナリオの特定のPhaseについてのみパラメータ推定を行うことができます（時間の節約）。

また、`Scenario.get(列名, phase=Phase名, name=シナリオ名)`とすることで、`Scenario.summary()`から値を取り出すことができます。

```Python
for date in candidates:
    # 候補日を名称とするシナリオの作成
    snl_opt.clear(name=date)
    # 区切りの変更
    snl_opt.combine(phases=["0th", "1st"], name=date)
    snl_opt.separate(date=date, name=date)
    # パラメータ推定（0th/1st phaseのみ実施）
    snl_opt.estimate(cs.SIRF, phases=["0th", "1st"], name=date)
    # RMSLEの記録
    opt_dict[date]["0th"] = snl_opt.get("RMSLE", phase="0th", name=date)
    opt_dict[date]["1st"] = snl_opt.get("RMSLE", phase="1st", name=date)
```

データフレーム形式でRMSLEを表示します。pandasはCovsirPhyのインストール時に依存パッケージとしてインストールされています。

```Python
import pandas as pd
pd.DataFrame.from_dict(opt_dict, orient="index")
```

|           |      0th |     1st |
|:----------|---------:|--------:|
| 01Mar2020 | 0.399103 | 5.54859 |
| 12Apr2020 | 0.757649 | 1.46627 |

1st phaseの開始日を12Apr2020としたほうが01Mar2020とした場合よりも1st phaseのRMSLEを抑えられるようです。しかし0th phaseのRMSLEは上昇しており、最適な区切りは02Mar2020から11Apr2020の間にあるようです。（この先については長くなってきたので省略します...）

## 12. あとがき
表が多く記事が長くなってしまいましたが、今回も閲覧ありがとうございました！

次回は未来のphaseを追加し、患者数のシュミレーションを実行する方法についてご説明します。
