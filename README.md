# kakuyomu_LaTeX
カクヨムに投稿されている作品をLuaLaTeXでPDF製本を行うpythonプログラムです。

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

このプログラムを動かす為に必要なpythonモジュールは以下の物です。もしインストールしていないモジュールがある場合、pip3でインストール後に使用してください。

- requests
- pathlib
- bs4 (BeautifulSoup)
- re
- time

```
pip3 install <"module name">
```

## 使い方
Microsoft PowerShellなどのCUIで以下を実行してください。
### カクヨムの作品をダウンロードする場合
```
$(任意)/kakuyomu_LuaLaTeX python3 kakuyomu_LuaLaTeX.py

(中略)

(メインページのURLを貼る)
https://kakuyomu.jp/works/XXXXXXXXXXXXXX
```

### 小説家になろうの作品をダウンロードする場合
```
$(任意)/kakuyomu_LuaLaTeX python3 narou_LuaLaTeX.py

(中略)

(メインページのURLを貼る)
https://ncode.syosetu.com/nXXXXX/
```

## ライセンス
このリポジトリにある全てのプログラムはMITライセンスを持ちます。

## 予想されるエラー



- メインページのURLを入力したのに、プログラムが動かない
    - 小説のタイトルが長すぎる場合、Windowsでは動かない可能性があります。

    - URLの再確認をしてください。URL末尾がコピー出来ていないなどはありませんか？

- コンパイルが通らない。出力されたPDFに変な文章が存在する。 PDFを開くことが出来ない。
    - 必要な.styファイルなどが入っていない可能性があります。
        sty_filesに必要な.styファイルがあるかどうか確認してください。

    - プログラム上の問題である可能性が高いです。
        ダウンロードしようとしたURL、エラーログなどを保存して、ご一報ください。