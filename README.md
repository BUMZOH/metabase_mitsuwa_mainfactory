# Metabase（光和工業 本社工場 見える化）

工場データを Metabase Community Edition で可視化するための環境です。

Metabase単体では不足する表示機能については、Flaskアプリを併用します。

---

# システム構成

```text
NAS上のSQLite
        │
        │  直接参照
        ▼
     Metabase
        │
        ├── ダッシュボード表示
        │
        └── URLクリック
                │
                ▼
          Flaskアプリ
                │
                ▼
              Chrome
```

SQLiteデータベースは、NAS上のファイルをMetabaseから直接参照します。

起動時にローカルへコピーする方式は使用しません。

これにより、Metabaseダッシュボードの自動更新を実行した際に、NAS上の最新データを表示できます。

Metabase本体には工場データそのものは保存されません。

---

# SQLiteデータベースの保存場所

Metabaseは次のNAS上のSQLiteデータベースを直接参照します。

```text
\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db
```

NASやネットワークに接続できない場合、ダッシュボードのデータ取得は失敗します。

---

# フォルダ構成

```text
metabase_mitsuwa_mainfactory/
│
├── .venv/
│
├── flask_display_timeline/
│   └── Flaskアプリ一式
│
├── plugins/
│
├── metabase.db.mv.db
├── metabase.jar
├── start_all.bat
├── .gitignore
├── CHANGELOG.md
└── README.md
```

`Data`フォルダは使用しません。

SQLiteデータベースはNAS上のファイルを直接参照します。

---

# Git管理

## 管理対象

- `metabase.db.mv.db`
- `start_all.bat`
- `flask_display_timeline/`
- `plugins/`
- `.gitignore`
- `README.md`
- `CHANGELOG.md`

## 管理対象外

- `metabase.jar`
- `.venv/`
- NAS上のSQLiteデータ
- Pythonのキャッシュ
- ログファイル
- 一時ファイル
- Flaskの秘密情報を保存する`.env`

---

# metabase.db.mv.dbについて

このファイルにはMetabaseの設定が保存されています。

主な内容は次のとおりです。

- 保存済みSQL
- 質問
- ダッシュボード
- レイアウト
- フィルター設定
- データベース接続情報
- ユーザー設定

Git管理することで、Metabase環境の最新版を保存できます。

ただし、バイナリファイルのため、Git上で内容の差分を確認することはできません。

---

# metabase.jarについて

`metabase.jar`はGitでは管理しません。

容量が非常に大きいため、必要に応じてMetabase公式サイトからダウンロードして配置します。

使用するMetabaseのバージョンは、READMEまたはCHANGELOGへ記録します。

---

# SQLiteデータについて

工場データはNAS上のSQLiteデータベースに保存されています。

Metabaseは次のファイルを直接参照します。

```text
\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db
```

SQLiteデータそのものはGit管理しません。

## NASを直接参照する理由

以前は、Metabase起動時にNAS上のSQLiteデータベースをローカルへコピーしていました。

しかし、その方式ではMetabaseの自動更新を実行しても、起動時にコピーした古いデータベースを再読込するだけでした。

現在はNAS上のSQLiteデータベースを直接参照するため、ダッシュボードの自動更新によって最新データを取得できます。

## 注意点

NAS上のデータを全件表示すると、ネットワーク転送の影響で表示に時間がかかる場合があります。

ダッシュボードでは、次のように取得対象を絞るSQLを使用します。

- 生産日で絞る
- 設備番号で絞る
- 必要なカラムだけ取得する
- 不要なBLOBカラムを取得しない
- 一覧表示では`LIMIT`を使用する

日付や設備を絞った通常のダッシュボードSQLでは、実用上十分な速度で動作します。

---

# 初回セットアップ

## 1. Javaのインストール

Metabaseの実行に必要なJavaをインストールします。

推奨環境：

```text
Java 21（Temurin）
```

---

## 2. Metabaseの配置

Metabase公式サイトから`metabase.jar`をダウンロードし、プロジェクトフォルダ直下へ配置します。

```text
metabase_mitsuwa_mainfactory/
└── metabase.jar
```

---

## 3. SQLite Driverの配置

必要なSQLite Driverを`plugins`フォルダへ配置します。

```text
metabase_mitsuwa_mainfactory/
└── plugins/
```

---

## 4. Python仮想環境の作成

Flaskアプリ用のPython仮想環境を、プロジェクトフォルダ直下へ作成します。

```text
metabase_mitsuwa_mainfactory/
└── .venv/
```

必要なPythonパッケージをインストールします。

---

## 5. NAS接続の確認

次のSQLiteデータベースへアクセスできることを確認します。

```text
\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db
```

NASへ接続できない状態では、Metabaseのダッシュボードからデータを取得できません。

---

## 6. Metabaseのデータベース接続設定

Metabaseの管理画面から、SQLiteデータベースの接続先を設定します。

```text
管理
↓
データベース
↓
本社工場稼働データ
↓
編集
```

`Filename`へ次のパスを設定します。

```text
\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db
```

MetabaseはSQLiteの接続先を絶対パスで保存します。

---

## 7. 起動

次のバッチファイルを実行します。

```text
start_all.bat
```

`start_all.bat`は、おおむね次の順番で処理します。

1. 必要なファイルの存在確認
2. NAS上のSQLiteデータベースの存在確認
3. Flaskアプリの起動
4. Metabaseの起動
5. ChromeでMetabaseを開く

ブラウザでは次のURLを開きます。

```text
http://localhost:3000
```

---

# ダッシュボードの自動更新

Metabaseダッシュボードでは、自動更新間隔を設定できます。

例：

- 1分
- 5分
- 10分
- 15分
- 30分
- 60分

NAS上のSQLiteデータベースを直接参照しているため、自動更新のたびに最新データを再取得できます。

ただし、SQLiteへデータを書き込んでいる最中やNASの通信状態によっては、一時的に取得が遅くなる可能性があります。

---

# 生産日の切り替えについて

このシステムでは、カレンダー上の日付が午前0時になった時点では、生産日は切り替わりません。

`production_date`は午前4時に更新されます。

そのため、例えば次の状態が発生します。

```text
update_at       : 2026-07-31 02:10:05
production_date : 2026-07-30
```

午前4時より前のデータを確認する場合は、ダッシュボードの日付フィルターで前日の`production_date`を指定します。

---

# 別PCへ移植する場合

GitHubから次のファイルを取得します。

- `metabase.db.mv.db`
- `start_all.bat`
- `flask_display_timeline/`
- `plugins/`
- `.gitignore`
- `README.md`
- `CHANGELOG.md`

別途、次のものを用意します。

- `metabase.jar`
- `.venv`またはPython仮想環境
- Flaskアプリに必要なPythonパッケージ
- 必要に応じて`.env`

移植先PCからNAS上のSQLiteデータベースへアクセスできることも確認します。

---

## SQLiteの接続先を再確認

別PCへ移植した場合は、Metabaseのデータベース接続設定を確認します。

```text
管理
↓
データベース
↓
本社工場稼働データ
↓
編集
```

`Filename`が次のNASパスになっていることを確認します。

```text
\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl\operation_data\main_factory_production_data.db
```

---

# Gitへコミットする前

必ずMetabaseを終了してください。

```text
Metabase終了
    ↓
git status
    ↓
git add
    ↓
git commit
```

起動中の`metabase.db.mv.db`をコミットすることは推奨しません。

Metabase終了後にファイルの更新が完了してからコミットします。

---

# バージョン管理

ダッシュボードやシステム構成が一区切りついたタイミングでコミットします。

例：

- 第1工場完成
- 第3工場追加
- 第4工場追加
- フィルター改善
- Flask連携追加
- NAS直接参照へ変更
- 自動更新対応
- Metabaseアップデート前

変更内容は`CHANGELOG.md`にも記録します。

---

# 備考

本リポジトリは、「工場見える化」のMetabase環境とFlask連携部分を管理します。

工場データであるSQLiteデータベースそのものは管理対象外です。

ダッシュボードでは、NAS上のSQLiteを直接参照し、Metabaseの自動更新機能によって最新データを表示します。
