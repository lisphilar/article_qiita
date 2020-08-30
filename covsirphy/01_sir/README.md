# [CovsirPhy] COVID-19データ解析用Pythonパッケージ: SIR model

## Introduction

COVID-19のデータ（PCR陽性者数など）のデータを簡単にダウンロードして解析できるPythonパッケージ [CovsirPhy](https://github.com/lisphilar/covid19-sir)を作成しています。パッケージを使用した解析例、作成にあたって得られた知識（Python, GitHub, Sphinx,...）に関する記事を今後公開する予定です。

英語版のドキュメントは[CovsirPhy: COVID-19 analysis with phase-dependent SIRs](https://lisphilar.github.io/covid19-sir/index.html), [Kaggle: COVID-19 data with SIR model](https://www.kaggle.com/lisphilar/covid-19-data-with-sir-model)にて公開しています。

**今回は基本モデルSIR modelについて紹介します。**実データは出てきません。
英語版：[Usage (details: theoretical datasets)](https://lisphilar.github.io/covid19-sir/usage_theoretical.html)

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
# '2.8.0'
```

||実行環境|
|:--:|:--:|
| OS | Windows Subsystem for Linux |
| Python | version 3.8.5 |

## 2. SIR modelとは
Susceptible（感受性保持者）がInfected（感染者）と接触したとき、感染する確率をEffective contact rate $\beta$ [1/min]と定義します。$\gamma$ [1/min]はInfectedからRecovered（回復者）に移行する確率です[^1][^2]。

[^1]: [Learning Scientific Programming with Python: The SIR epidemic model](https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/)  
[^2]: [Wikipedia: SIRモデル](https://ja.wikipedia.org/wiki/SIR%E3%83%A2%E3%83%87%E3%83%AB)  

```math
\begin{align*}
\mathrm{S} \overset{\beta I}{\longrightarrow} \mathrm{I} \overset{\gamma}{\longrightarrow} \mathrm{R}  \\
\end{align*}
```

## 3. 連立常微分方程式
総人口$N = S + I + R$として、

```math
\begin{align*}
& \frac{\mathrm{d}S}{\mathrm{d}T}= - N^{-1}\beta S I  \\
& \frac{\mathrm{d}I}{\mathrm{d}T}= N^{-1}\beta S I - \gamma I  \\
& \frac{\mathrm{d}R}{\mathrm{d}T}= \gamma I  \\
\end{align*}
```

## 4. 無次元パラメータ
このまま扱っても良いですが、パラメータの範囲を$(0, 1)$に限定するため無次元化します。今回の記事では出てきませんが、実データからパラメータを計算する際に効果を発揮します。

$(S, I, R) = N \times (x, y, z)$, $(T, \beta, \gamma) = (\tau t, \tau^{-1}\rho, \tau^{-1}\sigma)$, $1 \leq \tau \leq 1440$ [min]として、

```math
\begin{align*}
& \frac{\mathrm{d}x}{\mathrm{d}t}= - \rho x y  \\
& \frac{\mathrm{d}y}{\mathrm{d}t}= \rho x y - \sigma y  \\
& \frac{\mathrm{d}z}{\mathrm{d}t}= \sigma y  \\
\end{align*}
```

このとき、

```math
\begin{align*}
& 0 \leq (x, y, z, \rho, \sigma) \leq 1  \\
\end{align*}
```

## 5.（基本/実効）再生産数
（基本/実効）再生産数 Reproduction numberは次の通り定義されます[^3]。

[^3]: [Infection Modeling — Part 1 Estimating the Impact of a Pathogen via Monte Carlo Simulation](https://towardsdatascience.com/infection-modeling-part-1-87e74645568a)

```math
\begin{align*}
R_t = \rho \sigma^{-1} = \beta \gamma^{-1}
\end{align*}
```

### 6. データ例
パラメータ$(\rho, \sigma) = (0.2, 0.075)$及び初期値を設定してグラフ化します。

```Python
# Parameters
pprint(cs.SIR.EXAMPLE, compact=True)
# {'param_dict': {'rho': 0.2, 'sigma': 0.075},
# 'population': 1000000,
# 'step_n': 180,
# 'y0_dict': {'Fatal or Recovered': 0, 'Infected': 1000, 'Susceptible': 999000}}
```

（基本/実効）再生産数：

```Python
# Reproduction number
eg_dict = cs.SIR.EXAMPLE.copy()
model_ins = cs.SIR(
    population=eg_dict["population"],
    **eg_dict["param_dict"]
)
model_ins.calc_r0()
# 2.67
```

グラフ表示：

```Python
# Set tau value and start date of records
example_data = cs.ExampleData(tau=1440, start_date="01Jan2020")
# Add records with SIR model
model = cs.SIR
area = {"country": "Full", "province": model.NAME}
example_data.add(model, **area)
# Change parameter values if needed
# example_data.add(model, param_dict={"rho": 0.4, "sigma": 0.0150}, **area)
# Records with model variables
df = example_data.specialized(model, **area)
# Plotting
cs.line_plot(
    df.set_index("Date"),
    title=f"Example data of {model.NAME} model",
    y_integer=True,
    filename="sir.png"
)
```

![sir.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/151369/27d51fee-d9f8-3246-1b86-273c38a825a2.png)


## 7. 次回
基本モデルSIR modelをCOVID-19用に改変したモデルSIR-F modelについて紹介します。
