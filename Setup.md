# Metabase Mitsuwa Main Factory

# 新しいPCセットアップ手順

------------------------------------------------------------------------

## 概要

本資料は、新しいWindows PCへ 「Metabase Mitsuwa Main
Factory」をセットアップする手順をまとめたものである。

本資料の手順どおりに進めれば、

-   Metabase
-   Flask
-   Playwright

を含めた開発・運用環境を再現できる。

------------------------------------------------------------------------

# Step1 Java

## インストール

以下から Temurin JDK 21 (LTS) をインストールする。

https://adoptium.net/

推奨設定

-   Windows x64
-   JDK
-   Version 21 (LTS)
-   MSI Installer

インストール時は以下を有効にする。

-   Add to PATH
-   JAVA_HOME

## 動作確認

``` cmd
java --version
```

``` cmd
where java
```

------------------------------------------------------------------------

# Step2 Metabase

## metabase.jar を配置

**metabase.db.mv.db と metabase.jar
は必ず同じバージョンを使用すること。**

今回のシステムでは **Metabase v0.63.1.3** を使用。

旧PCから `metabase.jar` をコピーすることを推奨する。

## 配置場所

``` text
metabase_mitsuwa_mainfactory
│
├── metabase.jar
├── metabase.db.mv.db
├── plugins
└── start_all.bat
```

## 単体起動確認

``` cmd
java -jar metabase.jar
```

ブラウザで

    http://localhost:3000

へアクセス。

確認事項

-   ログインできる
-   ダッシュボード表示
-   SQLite接続
-   グラフ表示

------------------------------------------------------------------------

# Step3 Python

``` cmd
python --version
```

Python 3.11 を使用する。

------------------------------------------------------------------------

# Step4 仮想環境

``` cmd
cd C:\myProgram\GitHub\metabase_mitsuwa_mainfactory
python -m venv .venv
.venv\Scripts\activate
```

有効化後、プロンプト先頭に `(.venv)` が表示されればOK。

------------------------------------------------------------------------

# Step5 requirements

``` cmd
pip install -r requirements.txt
```

requirements.txt

``` text
Flask
playwright
Pillow
```

確認

``` cmd
pip list
```

------------------------------------------------------------------------

# Step6 動作確認

## Flask

``` cmd
python flask_display_timeline\app.py
```

## Playwright

キャプチャアプリを起動し、

-   日付設定
-   MachineNo切替
-   スクリーンショット保存

を確認。

## 全体起動

``` text
start_all.bat
```

確認事項

-   Metabase起動
-   Flask起動
-   Chrome起動
-   SQLite接続
-   ダッシュボード表示
-   タイムライン表示
-   スクリーンショット保存

------------------------------------------------------------------------

# トラブルシューティング

## java コマンドが見つからない

JavaまたはPATHを確認。

## No module named 'PIL'

``` cmd
pip install Pillow
```

## Flaskが起動しない

``` cmd
.venv\Scripts\activate
```

で仮想環境を有効化する。

## Metabaseが起動しない

-   Java21
-   metabase.jar
-   metabase.db.mv.db
-   plugins

を確認。

## SQLiteへ接続できない

NAS接続とDB_PATHを確認。

------------------------------------------------------------------------

# チェックリスト

-   [ ] Javaインストール
-   [ ] Java動作確認
-   [ ] metabase.jar配置
-   [ ] Metabase起動
-   [ ] ログイン確認
-   [ ] ダッシュボード表示
-   [ ] Pythonインストール
-   [ ] .venv作成
-   [ ] requirementsインストール
-   [ ] Flask起動
-   [ ] Playwright起動
-   [ ] start_all.bat動作確認

------------------------------------------------------------------------

最終更新: 2026-08-03
