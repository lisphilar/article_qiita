# [CovsirPhy] COVID-19データ解析用Pythonパッケージ: Data loading

## Introduction

COVID-19のデータ（PCR陽性者数など）のデータを簡単にダウンロードして解析できるPythonパッケージ [CovsirPhy](https://github.com/lisphilar/covid19-sir)を作成しています。

紹介記事：

- [SIR model](https://qiita.com/Lisphilar/items/ac5a5fda02d8359d6a94)
- [SIR-F model](https://qiita.com/Lisphilar/items/99c1e7673bc13d77dfcc)

英語版のドキュメントは[CovsirPhy: COVID-19 analysis with phase-dependent SIRs](https://lisphilar.github.io/covid19-sir/index.html), [Kaggle: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model)にて公開しています。

**今回はCOVID-19の実データをダウンロードする方法についてご説明します。**
英語版：

- [Installation and dataset preparation](https://lisphilar.github.io/covid19-sir/INSTALLATION.html)
- [Usage (quick version)](https://lisphilar.github.io/covid19-sir/usage_quick.html)

## 1. 実行環境
CovsirPhyは下記方法でインストールできます！  
Python 3.7以上, もしくはGoogle Colaboratoryをご使用ください。

- 安定版：`pip install covsirphy --upgrade`
- 開発版：`pip install "git+https://github.com/lisphilar/covid19-sir.git#egg=covsirphy"`

```Python
# データ表示用
from pprint import pprint
# CovsirPhy
import covsirphy as cs
cs.__version__
# '2.8.2'
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux |
| Python | version 3.8.5 |

本記事の表及びグラフは2020/9/11時点のデータを使用して作成しました。

## 2. まとめ
以下4行でデータをダウンロードできます。

```Python
data_loader = cs.DataLoader("input")
jhu_data = data_loader.jhu()
population_data = data_loader.population()
oxcgrt_data = data_loader.oxcgrt()
```

下記3種類のデータが[COVID-19 Data Hub](https://covid19datahub.io/)[^1]より自動で、"input"ディレクトリ（フォルダ）に保存されます。データ整形もよしなにやってくれます。

[^1]: Guidotti, E., Ardia, D., (2020), “COVID-19 Data Hub”, Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.

- 感染者数/回復者数/死亡者数に関する各国・各地域の時系列データ
- 各国・各地域の人口データ
- [Oxford Covid-19 Government Response Tracker (OxCGRT)](https://github.com/OxCGRT/covid-policy-tracker): COVID-19に対する各国の対策状況を数値化したデータ

データ整形はCovsirPhy側で行っていますが、データのダウンロード自体は[COVID-19 Data Hub](https://covid19datahub.io/)公式のパッケージ`covid19dh`に依存しています。開発者の方とも連携[^2]してエラーが発生しないように努めていますが、何かあれば[CovsirPhyのissueページ](https://github.com/lisphilar/covid19-sir/issues)からご連絡ください！

[^2]: [GitHub issue: CovsirPhy (Python package for COVID-19 analysis) will use COVID-19 Data Hub #87](https://github.com/covid19datahub/COVID19/issues/87)

## 3. DataLoader class
データのダウンロードと整形を行うユーザーインターフェイスです。以下のように第1引数に"input"と与えると、各データが"input"ディレクトリにダウンロードされます。

```Python
data_loader = cs.DataLoader("input")
```

ディレクトリ名は変更可能です。第1引数のデフォルトは"input"となっており、省略も可能です。


## 4. DataLoader.jhu()
「感染者数/回復者数/死亡者数に関する各国・各地域の時系列データ」をダウンロードするメソッドです。最新データがダウンロードされていない場合のみダウンロードを実行します。ダウンロード済の場合は保存データの読み込みと整形のみ行います。

```Python
# verbose=True: ダウンロード時データの引用元を表示
jhu_data = data_loader.jhu(verbose=True)
type(jhu_data)
# -> <class 'covsirphy.cleaning.jhu_data.JHUData'>
```

もともとジョンズ・ホプキンス大学のデータを直接ダウンロードしていた関係で"jhu"というメソッド名を使っています。

データの引用元[^3]は`DataLoader`のインスタンスから確認できます。

[^3]: [COVID-19 Data Hub](https://covid19datahub.io/)は二次データです！ジョンズ・ホプキンス大学のデータなどをもとに、欠損値処理などの前処理をデータベース側で行ってくれています。大変感謝。

```Python
# COVID-19 DataHubの情報 -> (出力結果は省略)
print(jhu_data.citation)
# データの引用元リスト -> (出力結果は省略)
print(data_loader.covid19dh_citation)
# ダウンロードしたデータを表示(pandas.DataFrame) -> (出力結果は省略)
jhu_data.raw.tail()
```

`JHUData.cleaned()`により、日付/国名/地域名/確定症例数（PCR陽性者数）累計/現在の感染者数/死亡者数累計/回復者数累計のデータをデータフレーム形式(`pandas.DataFrame`)で取得できます。

```Python
jhu_data.cleaned().tail()
```

|        | Date       | Country   | Province   |   Confirmed |   Infected |   Fatal |   Recovered |
|-------:|:-----------|:----------|:-----------|------------:|-----------:|--------:|------------:|
| 211098 | 2020-09-07 | Colombia  | Vichada    |          14 |          0 |       0 |          14 |
| 211099 | 2020-09-08 | Colombia  | Vichada    |          14 |          0 |       0 |          14 |
| 211100 | 2020-09-09 | Colombia  | Vichada    |          14 |          0 |       0 |          14 |
| 211101 | 2020-09-10 | Colombia  | Vichada    |          14 |          0 |       0 |          14 |
| 211102 | 2020-09-11 | Colombia  | Vichada    |          14 |          0 |       0 |          14 |

国によっては国全体の値と地方ごとの値が両方登録されていますので、`jhu_data.cleaned().groupby("Country").sum()`では国別の正しい集計データを取得できません。そのため特定の国や地域のデータを取り出すメソッド`JHUData.subset(country, province)`を用意しました。出力結果からは国名と地域名の列が省略されます。

```Python
# 国名のみ選択 -> (出力結果は省略)
jhu_data.subset(country="Japan")
# 国名についてはISO3コードでもOK -> (出力結果は省略)
jhu_data.subset(country="JPN")
# 地方名も選択
jhu_data.subset(country="JPN", province="Tokyo").tail()
```

|     | Date       |   Confirmed |   Infected |   Fatal |   Recovered |
|----:|:-----------|------------:|-----------:|--------:|------------:|
| 172 | 2020-09-07 |       21849 |       2510 |     372 |       18967 |
| 173 | 2020-09-08 |       22019 |       2470 |     378 |       19171 |
| 174 | 2020-09-09 |       22168 |       2349 |     379 |       19440 |
| 175 | 2020-09-10 |       22444 |       2478 |     379 |       19587 |
| 176 | 2020-09-11 |       22631 |       2439 |     380 |       19812 |

注意：4次データ（都/国/有志の国内団体/COVID-19 Data Hub）であり、東京都発表の数値とは異なる場合があります。

時系列グラフを作成したい場合は`cs.line_plot()`関数をどうぞ（関数を非推奨にしてクラス化する可能性あり、検討中）。

```Python
cs.line_plot(
    subset_df.set_index("Date").drop("Confirmed", axis=1),
    title="Japan/Tokyo: cases over time",
    filename=None, # ファイルに出力する場合はファイル名を設定する
    y_integer=True, # y軸を整数値に。×10などを使用しない
)
```

![jhu_data_subset.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/1979c047-789d-7562-e11a-a41de25cc342.jpeg)

さらに、全世界の合計値を取得するメソッド`JHUData.total()`もご用意しました。割合データ付きです。

```Python
jhu_data.total().tail()
```

| Date                |   Confirmed |    Infected |   Fatal |   Recovered |   Fatal per Confirmed |   Recovered per Confirmed |   Fatal per (Fatal or Recovered) |
|:--------------------|------------:|------------:|--------:|------------:|----------------------:|--------------------------:|---------------------------------:|
| 2020-09-07 | 2.71499e+07 | 8.06515e+06 |  890441 | 1.81943e+07 |             0.0163986 |                  0.335071 |                        0.0466573 |
| 2020-09-08 | 2.73868e+07 | 8.10302e+06 |  895203 | 1.83886e+07 |             0.0163437 |                  0.33572  |                        0.0464225 |
| 2020-09-09 | 2.76653e+07 | 8.15167e+06 |  901058 | 1.86126e+07 |             0.016285  |                  0.336388 |                        0.0461758 |
| 2020-09-10 | 2.7954e+07  | 8.2298e+06  |  906678 | 1.88175e+07 |             0.0162173 |                  0.33658  |                        0.0459678 |
| 2020-09-11 | 2.79547e+07 | 8.22937e+06 |  906696 | 1.88187e+07 |             0.0162172 |                  0.336592 |                        0.045966  |

## 5. DataLoader.population()
「各国・各地域の人口データ」を1日単位で取得するメソッドです。

```Python
population_data = data_loader.population()
print(type(population_data))
# -> <class 'covsirphy.cleaning.population.PopulationData'>
```

`PopulationData.cleaned()`により、ISO3コード/国名/地域名/日付/人口のデータを取得できます。また各国/各地域の値の取得には`PopulationData.value(country, province)`をご使用ください。

```Python
# データフレーム形式で整形データを取得 -> 出力結果は省略
population_data.cleaned().tail()
# 国名のみ選択 -> int
population_data.value(country="Japan")
# 国名についてはISO3コードでもOK -> int
population_data.value(country="JPN")
# 地方名も選択 -> int
population_data.value(country="JPN", province="Tokyo")
```

人口の値は`PopulationData.update(value, country, province)`メソッドで更新できます。

```Python
# 更新前 -> 13942856
population_data.value(country="Japan", province="Tokyo")
# 更新
# https://www.metro.tokyo.lg.jp/tosei/hodohappyo/press/2020/06/11/07.html
population_data.update(14_002_973, "Japan", province="Tokyo")
# 更新後 -> 14002973
population_data.value("Japan", province="Tokyo")
```

## 6. DataLoader.oxcgrt()
「[Oxford Covid-19 Government Response Tracker (OxCGRT)](https://github.com/OxCGRT/covid-policy-tracker): COVID-19に対する各国の対策状況を数値化したデータ」を1日単位で取得するメソッドです。データの詳細についてはリンクをご確認ください。データをどのように解析に用いるかについては別記事でご紹介する予定ですが、現在も模索中です。

```Python
oxcgrt_data = data_loader.oxcgrt()
print(type(oxcgrt_data))
# -> <class 'covsirphy.cleaning.oxcgrt.OxCGRTData'>
```

`OxCGRTData.cleaned()`により、ISO3コード/国名/日付/各Indexのデータを取得できます。地域ごとのデータは含まれていません。`OxCGRTData.subset(country)`も地域名は指定できません。

```Python
# データフレーム形式で整形データを取得 -> 出力結果は省略
oxcgrt_data.cleaned().tail()
# 国名のみ選択可能
oxcgrt_data.subset(country="Japan")
# 国名についてはISO3コードでもOK
oxcgrt_data.subset(country="JPN")
```

|     | Date                |   School_closing |   Workplace_closing |   Cancel_events |   Gatherings_restrictions |   Transport_closing |   Stay_home_restrictions |   Internal_movement_restrictions |   International_movement_restrictions |   Information_campaigns |   Testing_policy |   Contact_tracing |   Stringency_index |
|----:|:--------------------|-----------------:|--------------------:|----------------:|--------------------------:|--------------------:|-------------------------:|---------------------------------:|--------------------------------------:|------------------------:|-----------------:|------------------:|-------------------:|
| 247 | 2020-09-07 |                1 |                   1 |               1 |                         0 |                   0 |                        1 |                                1 |                                     3 |                       2 |                2 |                 1 |              30.56 |
| 248 | 2020-09-08 |                1 |                   1 |               1 |                         0 |                   0 |                        1 |                                1 |                                     3 |                       2 |                2 |                 1 |              30.56 |
| 249 | 2020-09-09 |                1 |                   1 |               1 |                         0 |                   0 |                        1 |                                1 |                                     3 |                       2 |                2 |                 1 |              30.56 |
| 250 | 2020-09-10 |                1 |                   1 |               1 |                         0 |                   0 |                        1 |                                1 |                                     3 |                       2 |                2 |                 1 |              30.56 |
| 251 | 2020-09-11 |                1 |                   1 |               1 |                         0 |                   0 |                        1 |                                1 |                                     3 |                       2 |                2 |                 1 |              30.56 |

## 7. あとがき
今回はCovsirPhyを用いて各データを取得する方法をご説明しました。短いコードで簡単に取得できるようにがんばりましたので、ぜひご使用ください！フィードバックもお待ちしております。

次回は実データを用いた解析方法の説明について記事を作成する予定です。使用例に加えて、なるべく技術的なバックグラウンドについても記載しようと思います。よろしくお願いします！

お疲れさまでした！
