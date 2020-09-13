# [CovsirPhy] COVID-19データ解析用Pythonパッケージ: Parameter estimation

## Introduction

COVID-19のデータ（PCR陽性者数など）のデータを簡単にダウンロードして解析できるPythonパッケージ [CovsirPhy](https://github.com/lisphilar/covid19-sir)を作成しています。

紹介記事：

- [SIR model](https://qiita.com/Lisphilar/items/ac5a5fda02d8359d6a94)
- [SIR-F model](https://qiita.com/Lisphilar/items/99c1e7673bc13d77dfcc)
- [Data loading](https://qiita.com/Lisphilar/items/34337bd89ad485ec4a4b)
- [S-R trend analysis](https://qiita.com/Lisphilar/items/a0754e978172f20f6c4a)

**今回はParameter estimation（SIR-F modelなどのパラメータ推定）のご紹介です。**

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
本記事の表及びグラフは2020/9/12時点のデータを使用して作成しました。実データを[COVID-19 Data Hub](https://covid19datahub.io/)[^1]よりダウンロードするコード[^2]はこちら：

[^1]: Guidotti, E., Ardia, D., (2020), “COVID-19 Data Hub”, Journal of Open Source Software 5(51):2376, doi: 10.21105/joss.02376.
[^2]: [[CovsirPhy] COVID-19データ解析用Pythonパッケージ: Data loading](https://qiita.com/Lisphilar/items/34337bd89ad485ec4a4b)

```Python
data_loader = cs.DataLoader("input")
jhu_data = data_loader.jhu()
population_data = data_loader.population()
```

また、下記コードにより実データの確認とS-R trend analysis（感染拡大状況のトレンドの分析法）[^3]を実行してください。

[^3]: [[CovsirPhy] COVID-19データ解析用Pythonパッケージ: S-R trend analysis](https://qiita.com/Lisphilar/items/a0754e978172f20f6c4a)

```Python
# (Optional) 厚生労働省データの取得
japan_data = data_loader.japan()
jhu_data.replace(japan_data)
print(japan_data.citation)
# 解析用クラスのインスタンス生成
snl = cs.Scenario(jhu_data, population_data, country="Japan")
# 実データの確認
snl.records(filename=None)
# S-R trend analysis
snl.trend(filename=None)
# Phase設定の確認
snl.summary()
```

実データのグラフ：
![records.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/3caf1429-956a-8c87-82ed-85efa5472c23.jpeg)

S-R trend analysis:
![trend.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/93f5130f-fedf-ffcf-1912-4aee7c55e393.jpeg)

Phase設定：

|     | Type   | Start     | End       |   Population |
|:----|:-------|:----------|:----------|-------------:|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 |
| 1st | Past   | 22Apr2020 | 04Jul2020 |    126529100 |
| 2nd | Past   | 05Jul2020 | 23Jul2020 |    126529100 |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 |
| 5th | Past   | 15Aug2020 | 29Aug2020 |    126529100 |
| 6th | Past   | 30Aug2020 | 12Sep2020 |    126529100 |

## 3. 実行例
S-R trend analysisにより、"Phase"（パラメータが一定となる期間）に分割することができました。本記事では、各"Phase"のデータ（例えば0th phaseであれば2020/2/6 - 2020/4/21のデータ）を用いてパラメータの値を推定します。

推定のしくみについては別記事を作成する予定です。`optuna`パッケージを使ってパラメータの値を提案、`scipy.integrate.solve_ivp`によって数値解を計算、実データとの誤差の少ないパラメータセットを選び出しています。

結果の見方は後述しますが、下記2行で実行・結果一覧の取得ができます。今回はSIR-F model[^4]を使用しました。

[^4]: [[CovsirPhy] COVID-19データ解析用Pythonパッケージ: SIR-F model](https://qiita.com/Lisphilar/items/99c1e7673bc13d77dfcc)

```Python
# Parameter estimation with SIR-F model
snl.estimate(cs.SIRF)
# パラメータ一覧の取得
snl.summary()
```

```
# 標準出力の例（CPU数などによって処理時間は異なる）
# 詳細後述：最新のPhase = 6th phaseにてtauを含めた推定を行った後、tauを固定して0-5thのパラメータ推定
<SIR-F model: parameter estimation>
Running optimization with 8 CPUs...
        6th phase (30Aug2020 - 12Sep2020): finished  704 trials in 0 min 25 sec
        5th phase (15Aug2020 - 29Aug2020): finished  965 trials in 1 min  0 sec
        3rd phase (24Jul2020 - 01Aug2020): finished  965 trials in 1 min  0 sec
        1st phase (22Apr2020 - 04Jul2020): finished  913 trials in 1 min  0 sec
        4th phase (02Aug2020 - 14Aug2020): finished  969 trials in 1 min  0 sec
        0th phase (06Feb2020 - 21Apr2020): finished  853 trials in 1 min  0 sec
        2nd phase (05Jul2020 - 23Jul2020): finished  964 trials in 1 min  0 sec
Completed optimization. Total: 1 min 27 sec
```

|     | Type   | Start     | End       |   Population | ODE   |   Rt |       theta |       kappa |       rho |      sigma |   tau |   1/alpha2 [day] |   1/gamma [day] |   alpha1 [-] |   1/beta [day] |     RMSLE |   Trials | Runtime      |
|:----|:-------|:----------|:----------|-------------:|:------|-----:|------------:|------------:|----------:|-----------:|------:|-----------------:|----------------:|-------------:|---------------:|----------:|---------:|:-------------|
| 0th | Past   | 06Feb2020 | 21Apr2020 |    126529100 | SIR-F | 5.54 | 0.0258495   | 0.0002422   | 0.0322916 | 0.00543343 |   480 |             1376 |              61 |        0.026 |             10 | 1.17429   |      804 | 1 min  0 sec |
| 1st | Past   | 22Apr2020 | 04Jul2020 |    126529100 | SIR-F | 0.41 | 0.0730748   | 0.000267108 | 0.0118168 | 0.0264994  |   480 |             1247 |              12 |        0.073 |             28 | 1.11459   |      861 | 1 min  0 sec |
| 2nd | Past   | 05Jul2020 | 23Jul2020 |    126529100 | SIR-F | 2.01 | 0.000344333 | 7.92419e-05 | 0.0467789 | 0.023201   |   480 |             4206 |              14 |        0     |              7 | 0.0331522 |      910 | 1 min  0 sec |
| 3rd | Past   | 24Jul2020 | 01Aug2020 |    126529100 | SIR-F | 1.75 | 0.00169155  | 4.05087e-05 | 0.0459332 | 0.0260965  |   480 |             8228 |              12 |        0.002 |              7 | 0.0201773 |      923 | 1 min  0 sec |
| 4th | Past   | 02Aug2020 | 14Aug2020 |    126529100 | SIR-F | 1.46 | 0.000634554 | 0.000116581 | 0.0325815 | 0.0221345  |   480 |             2859 |              15 |        0.001 |             10 | 0.0751473 |      909 | 1 min  0 sec |
| 5th | Past   | 15Aug2020 | 29Aug2020 |    126529100 | SIR-F | 0.8  | 0.00244294  | 9.30884e-05 | 0.0272693 | 0.0337857  |   480 |             3580 |               9 |        0.002 |             12 | 0.0420563 |      907 | 1 min  0 sec |
| 6th | Past   | 30Aug2020 | 12Sep2020 |    126529100 | SIR-F | 0.69 | 5.36037e-05 | 0.000467824 | 0.0219379 | 0.0312686  |   480 |              712 |              10 |        0     |             15 | 0.0132161 |      724 | 0 min 25 sec |

## 4. パラメータ推定値
横に長いので順番に見ていきましょう。まずはパラメータの推定値です。

```Python
# cs.SIRF.PARAMETERS: SIR-F modelのパラメータ名リスト
cols = ["Start", "End", "ODE", "tau", *cs.SIRF.PARAMETERS]
snl.summary(columns=cols)
```

|     | Start     | End       | ODE   |   tau |       theta |       kappa |       rho |      sigma |
|:----|:----------|:----------|:------|------:|------------:|------------:|----------:|-----------:|
| 0th | 06Feb2020 | 21Apr2020 | SIR-F |   480 | 0.0258495   | 0.0002422   | 0.0322916 | 0.00543343 |
| 1st | 22Apr2020 | 04Jul2020 | SIR-F |   480 | 0.0730748   | 0.000267108 | 0.0118168 | 0.0264994  |
| 2nd | 05Jul2020 | 23Jul2020 | SIR-F |   480 | 0.000344333 | 7.92419e-05 | 0.0467789 | 0.023201   |
| 3rd | 24Jul2020 | 01Aug2020 | SIR-F |   480 | 0.00169155  | 4.05087e-05 | 0.0459332 | 0.0260965  |
| 4th | 02Aug2020 | 14Aug2020 | SIR-F |   480 | 0.000634554 | 0.000116581 | 0.0325815 | 0.0221345  |
| 5th | 15Aug2020 | 29Aug2020 | SIR-F |   480 | 0.000644851 | 0.000383424 | 0.0274104 | 0.0337156  |
| 6th | 30Aug2020 | 12Sep2020 | SIR-F |   480 | 5.36037e-05 | 0.000467824 | 0.0219379 | 0.0312686  |

SIR-F model[^4]:

```math
\begin{align*}
\mathrm{S} \overset{\beta I}{\longrightarrow} \mathrm{S}^\ast \overset{\alpha_1}{\longrightarrow}\ & \mathrm{F}    \\
\mathrm{S}^\ast \overset{1 - \alpha_1}{\longrightarrow}\ & \mathrm{I} \overset{\gamma}{\longrightarrow} \mathrm{R}    \\
& \mathrm{I} \overset{\alpha_2}{\longrightarrow} \mathrm{F}    \\
\end{align*}
```

$\alpha_2$, $\beta$, $\gamma$は「時間」を次元として有しています。この「時間」は連立常微分方程式$f'(T)=x(T)$を離散化した方程式$f(T+\Delta T) - f(T) = x(T) \Delta T$の$\Delta T$に依存しています。1日おきにデータを取得している以上$\Delta T$は1日（=1440 min）未満となりますが、具体的な値はわかりません。国や地域によって異なる可能性もあり、異なる国の有次元パラメータ$\alpha_2$, $\beta$, $\gamma$の比較を行うことは困難です。

そこで$\Delta T$に相当する変数$\tau$を設定し、有次元のパラメータを無次元化しました。

```math
\begin{align*}
(S, I, R, F) = & N \times (x, y, z, w)    \\
(T, \alpha_1, \alpha_2, \beta, \gamma) = & (\tau t, \theta, \tau^{-1}\kappa, \tau^{-1}\rho, \tau^{-1}\sigma)    \\
1 \leq \tau & \leq 1440    \\
\end{align*}
```

このとき[^4]、

```math
\begin{align*}
& 0 \leq (x, y, z, w, \theta, \kappa, \rho, \sigma) \leq 1  \\
\end{align*}
```

同一国内では$\tau$の値が一定となるように、最新のPhaseデータを用いて$\tau$と無次元パラメータを推定した後、他のPhaseのパラメータ推定時には同じ値を$\tau$として使用するようにしています。今回は表の通り480 minとなりました。計算を単純化するため1日=1440 minの約数を使用するようにプログラミングしています。

では、各無次元パラメータの推移をグラフ化してみましょう。

```math
\begin{align*}
& \frac{\mathrm{d}x}{\mathrm{d}t}= - \rho x y  \\
& \frac{\mathrm{d}y}{\mathrm{d}t}= \rho (1-\theta) x y - (\sigma + \kappa) y  \\
& \frac{\mathrm{d}z}{\mathrm{d}t}= \sigma y  \\
& \frac{\mathrm{d}w}{\mathrm{d}t}= \rho \theta x y + \kappa y  \\
\end{align*}
```

### rhoの推移
Susceptible（感受性保持者）がInfected（感染者）と接触したとき、感染する確率 $\rho$の推移：

```Python
snl.history(target="rho", filename=None)
```

![rho.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/7c997afd-5c69-8dd6-1ef4-62d41f14b08c.jpeg)


緊急事態宣言（区域限定2020/4/7, 全国2020/4/16, 全国で解除2020/5/25）の効果が4月後半に現れ、7月初旬まで維持されていた、と解釈しています。その後はね上がり、少しずつ低下してきています。詳細については議論が必要ですが、3密回避などの対策の効果が直接的に反映されるパラメータとなっています。

### sigmaの推移
InfectedからRecovered（回復者）に移行する確率 $\sigma$の推移：

```Python
snl.history(target="sigma", filename=None)
```

![sigma.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/6489fbb3-9891-b6dc-c52d-a5e98faa918c.jpeg)

4月後半に大きく上昇した後、上昇/下降を繰り返しながら上昇傾向にあります。医療提供体制、新薬の開発/供給状況が反映されるパラメータです。


### kappaの推移
感染者の死亡率$\kappa$の推移：

```Python
snl.history(target="kappa", filename=None)
```

![kappa.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/232713cf-c05d-42a0-9b96-1b2667eb2f3b.jpeg)

大きく変動しているように見えますが、値の絶対値が小さいため、ある程度一定に抑えられていると考えてよいのではないでしょうか（他国との比較による検証が必要）。医療体制を整え、新薬の十分な供給により$\kappa$を限りなく0に近づけていくことが必要です。

### thetaの推移
確定診断を受けた感染者のうち、確定診断の時点で亡くなっていた感染者の割合$\theta$の推移：

```Python
snl.history(target="theta", filename=None)
```

![theta.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/2c93eb2d-369a-d826-95e3-e78ee5258fb0.jpeg)

感染初期においては医療提供体制自体が極めて逼迫していたため解釈は難しいですが、検査が遅れて適切な治療を行えなかった場合などに値が上昇すると考えられます。

## 5. 有次元パラメータの推移
有次元のパラメータについても表に含まれています。解釈しやすくするため、もともと無次元の$\alpha_1$を除き、逆数にして単位を[day]にしています。

```Python
cols = ["Start", "End", "ODE", "tau", *cs.SIRF.DAY_PARAMETERS]
fh.write(snl.summary(columns=cols).to_markdown())
```

|     | Start     | End       | ODE   |   tau |   alpha1 [-] |   1/alpha2 [day] |   1/beta [day] |   1/gamma [day] |
|:----|:----------|:----------|:------|------:|-------------:|-----------------:|---------------:|----------------:|
| 0th | 06Feb2020 | 21Apr2020 | SIR-F |   480 |        0.026 |             1376 |             10 |              61 |
| 1st | 22Apr2020 | 04Jul2020 | SIR-F |   480 |        0.073 |             1247 |             28 |              12 |
| 2nd | 05Jul2020 | 23Jul2020 | SIR-F |   480 |        0     |             4206 |              7 |              14 |
| 3rd | 24Jul2020 | 01Aug2020 | SIR-F |   480 |        0.002 |             8228 |              7 |              12 |
| 4th | 02Aug2020 | 14Aug2020 | SIR-F |   480 |        0.001 |             2859 |             10 |              15 |
| 5th | 15Aug2020 | 29Aug2020 | SIR-F |   480 |        0.002 |             3580 |             12 |               9 |
| 6th | 30Aug2020 | 12Sep2020 | SIR-F |   480 |        0     |              712 |             15 |              10 |

有次元パラメータは無次元パラメータと同じ経過を示すため省略しますが、グラフは下記コードで取得できます。

```Python
# betaの場合 -> グラフ省略
snl.history(target="1/beta [day]", filename=None)
```

## 6. 実効産生産数の推移
SIR-F model[^4]の基本/実効産生産数Rtは次の通り定義しています。

```math
\begin{align*}
R_t = \rho (1 - \theta) (\sigma + \kappa)^{-1} = \beta (1 - \alpha_1) (\gamma + \alpha_2)^{-1}
\end{align*}
```

推移：

```Python
# 一覧
cols = ["Start", "End", "ODE", "tau", "Rt"]
snl.summary(columns=cols)
# グラフ
snl.history(target="Rt", filename="rt.jpg")
```
|     | Start     | End       | ODE   |   Rt |
|:----|:----------|:----------|:------|-----:|
| 0th | 06Feb2020 | 21Apr2020 | SIR-F | 5.54 |
| 1st | 22Apr2020 | 04Jul2020 | SIR-F | 0.41 |
| 2nd | 05Jul2020 | 23Jul2020 | SIR-F | 2.01 |
| 3rd | 24Jul2020 | 01Aug2020 | SIR-F | 1.75 |
| 4th | 02Aug2020 | 14Aug2020 | SIR-F | 1.46 |
| 5th | 15Aug2020 | 29Aug2020 | SIR-F | 0.8  |
| 6th | 30Aug2020 | 12Sep2020 | SIR-F | 0.69 |

![rt.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/9d1cafbf-01a5-15cd-dc38-2e631567ded4.jpeg)

$Rt > 1$が感染拡大の1つの目安となるため、水平線$Rt=1$を表示させました。

## 7. パラメータの正確性
パラメータの正確性を測るRMSLE score, パラメータを推定するために`optuna`パッケージが提案したパラメータセットの数、実行時間についても表に含まれています。

```Python
cols = ["Start", "End", "RMSLE", "Trials", "Runtime"]
snl.summary(columns=cols)
```

|     | Start     | End       |     RMSLE |   Trials | Runtime      |
|:----|:----------|:----------|----------:|---------:|:-------------|
| 0th | 06Feb2020 | 21Apr2020 | 1.17429   |      690 | 1 min  1 sec |
| 1st | 22Apr2020 | 04Jul2020 | 1.11459   |      764 | 1 min  0 sec |
| 2nd | 05Jul2020 | 23Jul2020 | 0.0331522 |      810 | 1 min  1 sec |
| 3rd | 24Jul2020 | 01Aug2020 | 0.0201773 |      816 | 1 min  1 sec |
| 4th | 02Aug2020 | 14Aug2020 | 0.0751473 |      808 | 1 min  0 sec |
| 5th | 15Aug2020 | 29Aug2020 | 0.0420563 |      804 | 1 min  0 sec |
| 6th | 30Aug2020 | 12Sep2020 | 0.0132161 |      658 | 0 min 25 sec |

RMSLE score (Root Mean Squared Log Error)[^5]の定義式は次の通りです。0に近いほど実データをよく反映していると言えます。省略しますが、推定方法の検証自体は理論データ（SIR-F modelの式とパラメータセットの例から理論的に作成される患者数データ）を使って行っております。

[^5]: [Please refer to What’s the Difference Between RMSE and RMSLE?](https://medium.com/analytics-vidhya/root-mean-square-log-error-rmse-vs-rmlse-935c6cc1802a)

```math
\begin{align*}
& \sqrt{\cfrac{1}{n}\sum_{i=1}^{n}(log_{10}(A_{i} + 1) - log_{10}(P_{i} + 1))^2}
\end{align*}
```

$A$は実データ, $P$は予測値を示しています。$i=1, 2, 3, 4(=n)$のとき、$A_i$及び$P_i$はそれぞれ$S, I, R, F$の実データ/予測値です。

値だけではイメージがつきにくいためグラフ化してみました。まずはRMSLE値が最も大きい0th phaseについて。1番上のグラフは実データと予測値の差、2, 3, 4番目は変数ごとに実データと予測値の両方を表示しています。

```Python
snl.estimate_accuracy(phase="0th", filename=None)
```

![accuracy_0th.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/51dbcb49-8497-123c-d21b-c42a3280e2a6.jpeg)

誤差がある程度生じています。`Scenario.separate()`などを使って0th phaseを分割したほうが良いようです（別記事を作成予定）。

一方でRMSLE scoreが最も小さい6th phaseでは実データと予測値がよく重なっています。

```Python
snl.estimate_accuracy(phase="6th", filename=None)
```

![accuracy_6th.jpg](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/e68f6451-52b6-9f2b-f70a-354a301ba182.jpeg)

## 8. あとがき
今回は各Phaseのパラメータを推定する方法についてご説明しました。流行開始から半年以上が経過し、パラメータの検証、今後のパラメータの予測、シナリオ分析が重要となる段階に来ていると思います。データサイエンスのテーマとしてCOVID-19の注目度が下がってきているようですが、データが蓄積されてきた分、ダッシュボードの作成に注力していた初期の頃より深い分析ができるようになってきました。

今回もお疲れさまでした！
