# HPCtoolkit ![Pull Request](https://img.shields.io/badge/Pull%20Requests-Welcome-brightgreen)
HPCを使用するときに、プログレスバーを表示するライブラリ

Pull Requests Welcome!

# 説明
exampleフォルダのようにHPCtoolkit使用すると、進捗がテキストファイルに記入される。

# デモ
以下のように、プログレスバーがリアルタイムで出力される。/iterは一回あたりの平均処理時間を意味する。

```progress_bar.txt
Start: 3/26 13:34
Expect: 
Active core: 8
Process: 8

0 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
1 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
2 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
3 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 27s/iter
4 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 27s/iter
5 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
6 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
7 [■■■■□□□□□□□□□□□□□□□□] 20% 0d 0h 0m 26s/iter
```
# 使い方

exapleフォルダに使用例がある。
定数をまとめたオブジェクトSIMに対して、lockを定義する。（同一ファイルに並列アクセスをするため）
``` Python
manager = multiprocessing.Manager()
SIM.lock = manager.Lock()
```
外側のforに対して、HPCtoolkit.Progressを使用する。
「-」 の部分を「+」の部分に書き換える
```diff
- for idx_En in range(0, len(SIM.EsN0)):
+ for idx_En in HPCtoolkit.Progress(range(0, len(SIM.EsN0)), SIM):
``` 

# インストール
```sh
pip install git+https://github.com/clcl777/HPCtoolkit.git
``` 
# Requirement
依存関係はない。

# VS.
tqdmを使用するのが一般的だが、なぜかHPCで使用するとリアルタイムで出力されなかったり、出力画面を全て見ることができない。

（明示的にフラッシュすればリアルタイムで出力できるかも　sys.stdout.flush()　）

tqdmにプルリク出してもだしてもよかったかも。

# リリースノート

v1.0 処理終了時間を予測する機能を作りたかったが、未実装
