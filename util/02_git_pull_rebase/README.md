# git pull実行時にNot possible to fast-forwardエラーが発生した場合の対応

## Contents
`git pull`を実行したときに`Not possible to fast-forward, aborting.`と表示され、ローカルをリモートリポジトリと同期できなくなった場合の対応方法です。


## 原因
リモートリポジトリの更新後、`git pull`(= `git fetch; git merge`)の前にローカルリポジトリを編集してcommitした場合などに発生するようです。

- Continuous integration (CI) toolを使った自動コミットが含まれる場合は要注意！
- pull requestをmergeした直後は要注意！


## 解決方法
落ち着いて、次の通り`git fetch`と`git rebase`を実行すれば副作用を抑えて解決できます[^1]。

[^1]: [stack overflow: Fatal: Not possible to fast-forward, aborting](https://stackoverflow.com/questions/13106179/fatal-not-possible-to-fast-forward-aborting)

master branchの場合：

```Bash
git pull origin master --rebase
```

Output:

```
From (remote repositoryのURL)
 * branch            master     -> FETCH_HEAD
Successfully rebased and updated refs/heads/master.
```

## コマンドのイメージ
リモートの変更内容をdiff-A, ローカルの変更内容をdiff-Bとしたとき[^2][^3]、

[^2]: [git pull --rebaseをpushする前にやろうという話。](https://qiita.com/makua/items/7aa1f4fa02ef9ab1f9d9)
[^3]: [git pull と git pull –rebase の違いって？図を交えて説明します！](https://kray.jp/blog/git-pull-rebase/)

ローカル側：
1. diff-Bをローカルから取り除く
2. diff-Aをローカルに反映させる
3. diff-Bをローカルに反映させる

リモート側：
1. diff-Bをリモートに反映させる

ローカル側もリモート側もdiff-A, diff-Bの順にcommitが設定されます。


## あとがき
「一時退避」などでがんばる方法もあると思いますが、履歴が複雑になります（経験談）。履歴を振り返りにくくなるのでrebaseすることをおすすめします。

またリモートとローカルで同じ場所を編集した場合はconflictが発生しますので、そちらも落ち着いて解決しましょう。

お疲れさまでした！
