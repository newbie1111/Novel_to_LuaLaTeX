# kakuyomu_LaTeX
カクヨムに投稿されている作品をLuaLaTeXでPDF製本を行うpythonプログラムです。

## 必要環境とモジュール

このプログラムを実行するには以下の環境が必要です。
- Python 3.8
- TeXLive 2017 又は TeXLive 2019

このプログラムを動かす為に必要なpythonモジュールは以下の物です。もしインストールしていないモジュールがある場合、pipでインストール後に使用してください。

- requests
- pathlib
- BeautifulSoup4
- re
- copy

```
pip install <"module name">
```

## 使い方
Microsoft PowerShellなどのCUIで以下を実行してください。

```
$(任意のパス)/kakuyomu_LuaLaTeX python3 kakuyomu_LuaLaTeX.py

(中略)

(メインページのURLを貼る)
https://kakuyomu.jp/works/XXXXXXXXXXXXXX
```

## ライセンス
このリポジトリにある全てのプログラムはMITライセンスを持ちます。

## 予想されるエラー

- メインページのURLを入力したのに、プログラムが動かない
    - 小説のタイトルが長すぎる場合、Windowsでは動かない可能性があります。
    - URLの再確認をしてください。URL末尾がコピー出来ていないなどはありませんか？

- コンパイルが通らない。
    - 必要な.styファイルなどが入っていない可能性があります。
        ```mktexlsr```してください。
    - プログラム上の問題である可能性が高いです。
        ダウンロードしようとしたURL、エラーログなどを保存して、ご一報ください。

- 出力されたPDFに変な文章が存在する。
    - プログラム上の問題である可能性が高いです。
        ダウンロードしようとしたURL、エラーログなどを保存して、ご一報ください。