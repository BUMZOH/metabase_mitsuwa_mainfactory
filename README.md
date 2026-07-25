# Metabase（光和工業 本社工場 見える化）

工場データを Metabase Community Edition で可視化するための環境です。

---

# システム構成

```
NAS(SQLite)
      │
      │  DBコピー
      ▼
Data/main_factory_production_data.db
      │
      ▼
Metabase
      │
      ▼
Chrome
```

SQLiteデータベースはNASからローカルへコピーして利用します。

Metabase本体には工場データは保存されません。

---

# フォルダ構成

```
metabase_mitsuwa_mainfactory/
│
├── Data/
│   └── main_factory_production_data.db
│
├── plugins/
│
├── metabase.db.mv.db
├── metabase.jar
├── start_metabase.bat
├── metabase-version.txt
├── .gitignore
└── README.md
```

---

# Git管理

## 管理対象

- metabase.db.mv.db
- start_metabase.bat
- plugins
- README.md
- metabase-version.txt

## 管理対象外

- metabase.jar
- Dataフォルダ内のSQLiteデータ
- ログファイル
- 一時ファイル

---

# metabase.db.mv.dbについて

このファイルにはMetabaseの設定が保存されています。

主な内容

- 保存済みSQL
- ダッシュボード
- レイアウト
- フィルター設定
- データベース接続情報
- ユーザー設定

Git管理することで、ダッシュボードの最新版を保存できます。

※ バイナリファイルのため差分表示はできません。

---

# metabase.jarについて

Gitでは管理しません。

容量が大きいため（約644MB）、必要に応じて公式サイトからダウンロードしてください。

使用バージョンは

```
metabase-version.txt
```

で管理します。

---

# SQLiteデータ

工場データはNASに保存されています。

起動時に

```
start_metabase.bat
```

が

```
Data/
```

へコピーします。

SQLiteデータはGit管理しません。

---

# 初回セットアップ

## 1. Javaインストール

Java 21 (Temurin)

---

## 2. Metabaseダウンロード

metabase-version.txt に記載されたバージョンの

```
metabase.jar
```

を配置します。

---

## 3. SQLite Driver配置

pluginsフォルダへ配置します。

---

## 4. SQLiteデータ配置

```
Data/
```

へSQLiteファイルを配置します。

---

## 5. 起動

```
start_metabase.bat
```

を実行します。

ブラウザが自動で

```
http://localhost:3000
```

を開きます。

---

# 別PCへ移植する場合

以下をGitHubから取得します。

- metabase.db.mv.db
- start_metabase.bat
- plugins
- README.md

別途

- metabase.jar
- SQLiteデータ

を配置してください。

---

## SQLiteの接続先を再設定

SQLiteの保存場所が変わった場合は

```
管理
↓
データベース
↓
main_factory_production_data
↓
編集
```

からSQLiteファイルの場所を再指定してください。

MetabaseはSQLiteの接続先を**絶対パス**で保存します。

---

# Gitへコミットする前

必ずMetabaseを終了してください。

```
Metabase終了
    ↓
git add
    ↓
git commit
```

起動中の

```
metabase.db.mv.db
```

をコミットすることは推奨しません。

---

# バージョン管理

ダッシュボードが一区切りついたタイミングでコミットします。

例

- 第1工場完成
- 第3工場追加
- 第4工場追加
- フィルター改善
- Metabaseアップデート前

---

# 備考

本リポジトリは

「工場見える化」

のMetabase環境のみを管理します。

工場データ(SQLite)そのものは管理対象外です。