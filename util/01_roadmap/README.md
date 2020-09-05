# Pythonパッケージ公開のロードマップ

Pythonパッケージを作成、公開する際に必要な手順の概要をまとめました。ツールの具体的な使用方法や詳細については参考となる資料へのリンクを後日追加、または別の記事を作成する予定です。

私自身2020年2月ごろにパッケージを公開しよう！と思い立ったのですが、何から始めればよいかわからず苦労しました。開発を進める中で得られた知見を今回まとめましたので、これから公開を考えていらっしゃる方の参考になれば幸いです！

また、過不足や他の方法がありましたらご教示ください。随時更新予定です。

対象となるパッケージ：
- Pythonのパッケージとして公開し、一般に使ってもらいたい
- GitHubなどでコードを公開し、ユーザーとも協議しながら開発を進めたい


## 概要

0. [内容の検討](#0-内容の検討)
1. [開発環境の整備](#1-開発環境の整備)
2. [コーディング](#2-コーディング)
3. [テストの運用](#3-テストの運用)
4. [ドキュメントの作成](#4-ドキュメントの作成)
5. [PyPIへの登録](#5-pypiへの登録)

## 0. 内容の検討
検討の必要な事項：
- ユーザー層：背景知識はどの程度必要か、Pythonや他のパッケージに関する知識はどの程度必要か
- 使用目的：ユーザーは何を得られるか
- 開発期間

ツール：
- マインドマップ
- アウトライン作成ツール：[WorkFlowy](https://workflowy.com/)


## 1. 開発環境の整備
ローカルPCに開発環境を構築しつつ、作成したコードを公開するしくみを整える必要があります。またGitを使用して変更履歴を随時記録することにより、開発状況を明確に把握できるようになります。

### リポジトリ（コードの保管場所）
[GitHub](https://github.com/)に開発用のRemote repositoryを作成し、ローカル環境にクローンして開発を行います。作業完了後、ローカル環境でコミットし、Remote repositoryにプッシュします。

- [GitとGithubの基礎](https://qiita.com/kibinag0/items/ec6583e4e7608c4d2add)

### Pythonの実行環境
Windows 10を使用している場合、可能であればWSL (Windows Subsystem for Linux)あるいはWSL2の使用をおすすめします。

- [WSLをインストールする](https://qiita.com/matarillo/items/61a9ead4bfe2868a0b86)

### Editorの導入
EditorもしくはIDE (Integrated Development Environment, 統合開発環境)をローカル環境に用意します。

Visual Studio Code (VScode)がおすすめです。多数のプラグインが用意されており、Git操作についてもより簡単に扱えるようになります。

### 依存パッケージの管理
pipenvやpoetryが有望のようです。pipenvを使用していますが、頻繁にエラーが出る&遅いため、poetryへの移行を検討中です。

### 開発ワークフロー
Git Flow, GitHub Flowなど、ブランチの使用方法やマージのタイミングについて色々な考え方があるようです。個人もしくは数人レベルで開発を行う場合は、そのなかでもシンプルな[Gitlab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)の使用をおすすめします。

また、GitHubのissue機能をtodo-list & 議論の場として使うと便利です。issueやpull requestには個別の番号が`#1`などと割り当てられますので、issue#1で問題提起し、issue番号をもとにブランチ`issue1`にて作業を行い、pull requestによりデフォルトのブランチにマージするという手順です。

- [Gitlab-flowの説明](https://qiita.com/tlta-bkhn/items/f2950aaf00bfb6a8c30d)
- [GitHub Issueの使い方 – 作成・書き方から閉じるまで【削除はできない】](https://howpon.com/8168)


### Versioning
大きな流れとして「開発版（GitHubで管理）」と「安定版（PyPIで管理）」の2本立てで開発を行うと便利かと思います。開発版は、上記開発フローによって作成します。

開発バージョンの名前の付け方はあまり定まったものはなさそうでした。私の場合は、マージが発生してissueを閉じた直後に開発版のバージョンを一つあげています。

バグ修正にてissue#2を閉じたとき：2.0.1-alpha.new.1 → 2.0.1-beta.new.1.fix.2

また、多数のissueが閉じた場合や安定版のバグを緊急に修正する必要が発生した場合は安定版のバージョンを[Semantic Versioning](https://semver.org/lang/ja/)にしたがってバージョンを上げてください。


## 2. コーディング
フォルダ構成などコーディング時に注意の必要な事項をまとめました。

### パッケージの名前
パッケージの1行説明文を英語で作成、そのなかからアルファベットを選んでパッケージ名にすると、あまり悩まなくて済むと思います。アルファベットの選び順については私は気にしてません（笑）

例：Python package for **COV**ID-19 anal**y**sis with **ph**ase-dependent **SIR**-derived ODE models = **CovsirPhy**

またGoogle検索を使って、他のサービス名と被らないようにしたほうが良いかもしれません。

インストール方法が変わるなど大騒動になるので、後から変更するのは難しいと思います。

### パッケージの識別情報
poetryを使用する場合は、別ファイルに記載することになりますが、pipenvを依存パッケージの管理に使用している場合は`setup.py`, `setup.cfg`というファイルをrepositoryのトップに作成してください。

```Python:setup.py
from setuptools import setup
setup()
```

```Python:setup.cfg
[metadata]
name = パッケージ名
version = attr: パッケージ名.__version__.__version__
url = レポジトリなどのURL
author = 著者名
author_email = メールアドレス
license = Apache License 2.0
license_file = LICENSE
description = パッケージの1行説明
long_description = file: README.rst
keywords = キーワード
classifiers =
    Development Status :: 5 - Production/Stable
    License :: OSI Approved :: Apache Software License
    Programming Language :: Python :: 3.7
    Programming Language :: Python :: 3.8


[options]
packages = find:
install_requires =
    # 依存パッケージ名
    numpy
    matplotlib
```

日本語で記載した部分やライセンス名などは適宜置き換えてください！
また、依存パッケージを追加した場合は随時"install_requires"欄への追加が必要となります。


### フォルダ構成
Repositoryのトップに、パッケージ名のフォルダ（またはsrcフォルダ）を作成してください。その中にまず、`__version__.py`及び`__init__.py`という空ファイルを作成してください。

そしてフォルダ構成（モジュール構成）を決めましょう。循環インポート[^1]を避けるため、`src/A/a1.py`を`src/B/b1.py`がインポートしかつ`src/B/b2.py`を`src/A/a2.py`がインポートする、ということが起こらないようにしましょう。開発環境ではエラーにならないが安定版をpip installするとエラーになる場合があるようで、苦労したことがあります。この修正だけのために2回バッチ番号を上げました。

[^1]: [Pythonで循環インポートするとどうなるのか](http://www.freia.jp/taka/blog/python-recursive-import/index.html)

`setup.cfg`ではなく`src/__version__.py`で管理すると、パッケージ内でもバージョン番号を取得・表示できるようになるので便利です。

```Python:__version__.py
__version__ = "0.1.0"
```

以下は`src/util/plotting.py`に`line_plot`という関数を作成した場合です。`from src.util.plotting import line_plot`と書くことにより、pip installした際に`from src.util.plotting import line_plot`ではなく`from src import line_plot`と呼び出せるようになります。

```Python:__init__.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# version
from src.__version__ import __version__
# util
from src.util.plotting import line_plot


def get_version():
    """
    Return the version number, like パッケージ名 v0.0.0
    """
    return f"パッケージ名 v{__version__}"


__all__ = ["line_plot"]
```

`__all__ = ["line_plot"]`と書くと、pylintなどのコード整形ツールの修正確認を回避できるようになります（pylintの設定を変更して修正確認を表示させないこともできますが）。また、`from src import *`とするだけで`line_plot`を使用できるようになります。ただし、`import *`は推奨されていません...


## 3. テストの運用

## 4. ドキュメントの作成

## 5. PyPIへの登録

## まとめ
