# Novel_to_LuaLaTeX
web小説投稿サイト「カクヨム」及び「小説化になろう」に投稿されている作品をダウンロードし、LuaLaTeXでPDF製本を行うpythonプログラムです。

## 環境とモジュール

このプログラムを実行が確認できた環境は以下の通りです。

### Windows
- Windows 10 Home または Education
- Python 3.8
- TeXLive 2017 又は TeXLive 2019

### Linux
- Windows Subsystem on Linux (Ubuntu 18.04.4 LTS)
- Python 3.6.9
- TeXLive 2019

### 実行前に確認すること
pythonのプログラムを起動する前に、以下のライブラリがインストールされているかどうかを確認してください。

- requests
- bs4 (BeautifulSoup)

```
pip3 install <"module name">
```

また、TeXのstyファイルが別途必要なので、広告鳥さんのブログから経由してインストールしてください。

- B6tate
- breakfbox
- uline--

TeX Liveを使用している場合、texmf-local内のlocalディレクトリにstyファイルを保存して、```mktexlsr```でstyファイルのリストを更新してから使用してください。


## 使い方
Microsoft PowerShellなどのCUIで以下を実行してください。
### カクヨムの作品をダウンロードする場合
```
$(任意)/kakuyomu_LuaLaTeX python3 ./pkg/kakuyomu_LuaLaTeX.py

(中略)

(メインページのURLを貼る)
https://kakuyomu.jp/works/XXXXXXXXXXXXXX
```

カレントディレクトリの`kakuyomu`ディレクトリ内に保存されます。

### 小説家になろうの作品をダウンロードする場合
```
$(任意)/kakuyomu_LuaLaTeX python3 ./pkg/narou_LuaLaTeX.py

(中略)

(メインページのURLを貼る)
https://ncode.syosetu.com/nXXXXX/
```

カレントディレクトリの`narou`ディレクトリ内に保存されます。

## ライセンス
このリポジトリにある全てのプログラムはMITライセンスを持ちます。

## 予想されるエラー

- メインページのURLを入力したのに、プログラムが動かない
    - URLの再確認をしてください。
    - 実行したプログラムが間違っていないか確認してください。
    - ライブラリがインストールされていないか、別のpythonにインストールされていないかを確認してください。


- コンパイルが通らない。出力されたPDFに変な文章が存在する。 PDFを開くことが出来ない。
    - 必要な.styファイルなどが入っていない可能性があります。
        sty_filesに必要な.styファイルがあるかどうか確認してください。

- 出力された文書に想定されていない文が存在する（HTML構文など）。
    明らかに文章が抜け落ちている
    - バグなので報告してください。

その他、何か問題がある場合は該当の作品URLを添付の上、報告していただけると幸いです。
