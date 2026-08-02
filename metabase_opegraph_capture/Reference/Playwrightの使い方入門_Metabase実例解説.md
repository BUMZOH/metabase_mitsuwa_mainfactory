# Playwrightの使い方入門  
## MetabaseをChromeで開くコードを実例に学ぶ

作成日: 2026-08-02

---

# 1. はじめに

この資料では、次のコードを実例として、Python版Playwrightの基本的な使い方を初心者向けに解説します。

```python
with sync_playwright() as playwright:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=browser_data_directory,
        channel="chrome",
        headless=False,
        viewport={
            "width": VIEWPORT_WIDTH,
            "height": VIEWPORT_HEIGHT,
        },
        ignore_default_args=[
            "--no-sandbox",
        ],
    )

    try:
        page = context.pages[0] if context.pages else context.new_page()

        print("Chromeを起動しています。")
        print("Metabaseが起動済みであることを確認してください。")
        page.goto(
            DASHBOARD_URL,
            wait_until="domcontentloaded",
            timeout=30_000,
        )
```

このコードは、Playwrightを使って次の処理を行っています。

```text
Playwrightを開始する
    ↓
Google Chromeを起動する
    ↓
専用のブラウザデータを読み込む
    ↓
既存のタブを取得する
    ↓
MetabaseのURLを開く
```

一見すると難しそうですが、処理を小さく分ければ理解できます。

---

# 2. Playwrightとは

Playwrightは、PythonなどのプログラムからWebブラウザを操作するためのライブラリです。

例えば、次のような操作を自動化できます。

- Chromeを起動する
- Webページを開く
- ボタンをクリックする
- 入力欄へ文字を入力する
- ページの表示を待つ
- スクリーンショットを保存する
- HTML要素の文字を取得する
- 複数ページを順番に処理する

今回のアプリでは、Metabaseのダッシュボードを設備番号ごとに開き、スクリーンショットを保存するために使っています。

---

# 3. Playwrightの基本的な登場人物

Playwrightのコードでは、主に次の4つが登場します。

```text
playwright
browser
context
page
```

今回のコードでは `browser` を直接作らず、`launch_persistent_context()` により `context` を直接作っています。

それぞれの役割は次のとおりです。

| 名前 | 役割 |
|---|---|
| `playwright` | Playwright全体を操作する入口 |
| `chromium` | Chromium系ブラウザを操作する機能 |
| `context` | ブラウザ内の独立した利用環境 |
| `page` | 1つのタブまたはページ |

イメージは次のとおりです。

```text
Playwright
└── Chromium系ブラウザ
    └── Browser Context
        ├── Page 1
        ├── Page 2
        └── Page 3
```

今回のコードでは、

```python
playwright.chromium.launch_persistent_context(...)
```

によって、ChromeとBrowser Contextをまとめて起動しています。

---

# 4. 同期APIと非同期API

Python版Playwrightには、大きく分けて2種類の使い方があります。

```text
同期API
非同期API
```

今回使っているのは同期APIです。

```python
from playwright.sync_api import sync_playwright
```

同期APIでは、上から順番に処理が進みます。

```python
page.goto(...)
page.screenshot(...)
```

初心者にとって読みやすく、通常の自動操作アプリでは扱いやすい書き方です。

一方、非同期APIでは `async` や `await` を使います。

```python
from playwright.async_api import async_playwright
```

```python
async with async_playwright() as playwright:
    ...
```

今回のアプリでは、複数の処理を同時並行で行う必要がないため、同期APIで十分です。

---

# 5. `with sync_playwright() as playwright:`

```python
with sync_playwright() as playwright:
```

この行は、Playwrightの利用を開始しています。

## 5.1 `sync_playwright()`

```python
sync_playwright()
```

これは、同期版Playwrightを起動するための処理です。

ただし、`sync_playwright()` を呼んだだけではなく、今回は `with` 文と組み合わせています。

---

## 5.2 `with` 文を使う理由

`with` 文には、処理の開始と終了を安全に管理する役割があります。

```python
with sync_playwright() as playwright:
    ...
```

このブロックに入るとPlaywrightが開始されます。

ブロックを抜けると、Playwrightの終了処理が自動で行われます。

イメージは次のとおりです。

```text
with開始
    ↓
Playwright起動
    ↓
ブラウザ操作
    ↓
with終了
    ↓
Playwright終了処理
```

手動で書くと、概念的には次のようになります。

```python
playwright_manager = sync_playwright()
playwright = playwright_manager.start()

try:
    ...
finally:
    playwright_manager.stop()
```

`with` 文を使う方が簡潔で安全です。

---

## 5.3 `as playwright`

```python
as playwright
```

Playwrightを操作するためのオブジェクトを、変数 `playwright` に受け取っています。

この変数から、Chromium、Firefox、WebKitなどへアクセスできます。

```python
playwright.chromium
playwright.firefox
playwright.webkit
```

今回使うのはChromium系ブラウザです。

```python
playwright.chromium
```

Google ChromeはChromium系ブラウザなので、この機能から起動します。

---

# 6. `launch_persistent_context()`

```python
context = playwright.chromium.launch_persistent_context(
    ...
)
```

この処理では、ブラウザを起動し、同時に永続的なBrowser Contextを作っています。

## 6.1 Browser Contextとは

Browser Contextは、ブラウザ内の独立した利用環境です。

次のような情報を持ちます。

- Cookie
- ログイン状態
- Local Storage
- セッション情報
- キャッシュ
- 複数のタブ

通常のChromeでいう「ユーザープロファイル」に近いものです。

---

## 6.2 persistentの意味

`persistent` は「永続的な」という意味です。

通常の一時的なBrowser Contextは、終了するとCookieやログイン情報が消えます。

一方、

```python
launch_persistent_context()
```

では、ブラウザデータをフォルダへ保存できます。

そのため、次回起動時に次の情報を再利用できます。

- Metabaseへのログイン状態
- Cookie
- 一部のサイト設定
- Local Storage

今回のアプリでは、毎回ログインし直す手間を減らすために使っています。

---

# 7. `context` に代入されるもの

```python
context = playwright.chromium.launch_persistent_context(...)
```

戻り値はBrowser Contextです。

この `context` から、次のような操作ができます。

```python
context.pages
context.new_page()
context.close()
```

| 操作 | 意味 |
|---|---|
| `context.pages` | 現在開いているページ一覧 |
| `context.new_page()` | 新しいタブを作る |
| `context.close()` | ブラウザ環境を閉じる |

今回のコードでは、後で `context.pages` と `context.new_page()` を使っています。

---

# 8. `user_data_dir`

```python
user_data_dir=browser_data_directory,
```

これは、Chromeのユーザーデータを保存するフォルダです。

例えば、今回のアプリでは次のようなフォルダを使っています。

```text
metabase_opegraph_capture/
└── playwright_browser_data/
```

このフォルダには、Playwrightが起動したChromeの利用情報が保存されます。

主な目的は、ログイン状態の維持です。

---

## 8.1 なぜ専用フォルダを使うのか

普段使っているChromeのプロファイルを直接使うと、Chromeがすでに起動している場合に競合する可能性があります。

そこで、Playwright専用のフォルダを作ります。

```python
browser_data_directory = (
    app_directory / "playwright_browser_data"
)
```

これにより、

```text
普段使うChrome
Playwrightが使うChrome
```

を分けられます。

---

## 8.2 Git管理しない理由

`playwright_browser_data` には、次のような情報が含まれる可能性があります。

- Cookie
- ログイン情報
- キャッシュ
- 環境固有のデータ
- 多数の自動生成ファイル

そのため、通常はGit管理しません。

`.gitignore` では、例えば次のように除外します。

```gitignore
**/playwright_browser_data/
```

---

# 9. `channel="chrome"`

```python
channel="chrome",
```

この指定により、Playwright付属のChromiumではなく、PCにインストールされているGoogle Chromeを使います。

## 9.1 `chromium` と Google Chrome

コードでは次のように書いています。

```python
playwright.chromium
```

ここでの `chromium` は、Chromium系ブラウザを操作する機能です。

そのうえで、

```python
channel="chrome"
```

を指定することでGoogle Chromeを選びます。

整理すると、

```text
playwright.chromium
    ↓
Chromium系ブラウザを扱う

channel="chrome"
    ↓
その中からGoogle Chromeを使う
```

となります。

---

## 9.2 `channel` を省略した場合

`channel="chrome"` を省略すると、通常はPlaywrightが管理するChromiumを使います。

```python
playwright.chromium.launch_persistent_context(
    user_data_dir=browser_data_directory,
)
```

今回のアプリでは、普段見慣れたGoogle Chromeを使うため、`channel="chrome"` を指定しています。

---

# 10. `headless=False`

```python
headless=False,
```

`headless` は、ブラウザ画面を表示するかどうかを指定します。

```text
headless=False
    → ブラウザ画面を表示する

headless=True
    → ブラウザ画面を表示しない
```

今回のアプリでは、ユーザーが次の操作を手動で行う可能性があります。

- Metabaseへのログイン
- 日付フィルターの設定
- ダッシュボード表示の確認

そのため、画面を表示する必要があります。

```python
headless=False
```

を使います。

---

## 10.1 headlessモードが向いている処理

次のような場合は `headless=True` が便利です。

- 完全自動処理
- サーバー上での実行
- 夜間バッチ
- 人が画面を確認しない処理

今回のように手動確認がある場合は、`False` の方が適しています。

---

# 11. `viewport`

```python
viewport={
    "width": VIEWPORT_WIDTH,
    "height": VIEWPORT_HEIGHT,
},
```

これは、Webページを表示する領域の大きさを指定しています。

今回の設定値は次のとおりです。

```python
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080
```

したがって、実際には次の指定になります。

```python
viewport={
    "width": 1920,
    "height": 1080,
}
```

---

## 11.1 viewportはウィンドウ全体ではない

`viewport` は、厳密にはブラウザの外枠全体ではなく、Webページを表示する領域です。

ブラウザには次のような部分があります。

```text
タイトルバー
アドレスバー
タブ
Webページ表示領域 ← viewport
```

スクリーンショットのレイアウトは、このviewportの影響を受けます。

---

## 11.2 なぜ固定するのか

画面サイズが毎回変わると、Metabaseのグラフ配置やカードサイズが変わる可能性があります。

そこで、表示サイズを固定します。

```text
毎回同じ画面幅
    ↓
毎回ほぼ同じレイアウト
    ↓
スクリーンショットを比較しやすい
```

自動スクリーンショットでは重要な設定です。

---

# 12. `ignore_default_args`

```python
ignore_default_args=[
    "--no-sandbox",
],
```

Playwrightはブラウザ起動時に、いくつかの起動オプションを自動で渡します。

`ignore_default_args` は、その標準オプションの一部を使わないようにする設定です。

今回のコードでは、

```text
--no-sandbox
```

という標準引数を除外しています。

---

## 12.1 初心者がまず理解すべきこと

この部分は、Playwrightの基本操作というより、ブラウザ起動時の細かな調整です。

最初は次の理解で十分です。

> Playwrightが自動で付けるChrome起動オプションのうち、`--no-sandbox` だけを除外している。

ただし、環境によってはこの指定が不要な場合もあります。

通常のWindowsデスクトップ環境では、特別な理由がなければ、まず省略して動作確認する方法もあります。

---

# 13. `try` ブロック

```python
try:
    ...
```

この `try` は、後で必ず `context.close()` を実行するために使われています。

全体では次のような構造です。

```python
context = ...

try:
    # ブラウザ操作
finally:
    context.close()
```

途中でエラーが発生しても、`finally` によりブラウザを閉じられます。

---

# 14. `context.pages`

```python
context.pages
```

これは、現在そのBrowser Context内で開いているページの一覧です。

型のイメージはリストです。

```python
[
    page1,
    page2,
    page3,
]
```

ページが1つだけなら、

```python
context.pages[0]
```

で最初のページを取得できます。

---

# 15. 条件式によるpage取得

```python
page = context.pages[0] if context.pages else context.new_page()
```

これは三項演算子です。

通常のif文で書くと次のようになります。

```python
if context.pages:
    page = context.pages[0]
else:
    page = context.new_page()
```

意味は次のとおりです。

```text
すでにページがある
    ↓
最初のページを使う

ページがない
    ↓
新しいページを作る
```

---

## 15.1 なぜ既存ページを使うのか

`launch_persistent_context()` でChromeを起動すると、最初からページが1つ作られている場合があります。

その場合、さらに `new_page()` を呼ぶと余計なタブが増えます。

そこで、

```python
context.pages[0]
```

が使えるなら、それを再利用します。

---

## 15.2 `context.pages` の真偽判定

Pythonでは、空のリストは偽として扱われます。

```python
[]
```

は `False` 相当です。

要素のあるリストは真です。

```python
[page]
```

は `True` 相当です。

したがって、

```python
if context.pages:
```

は、

```text
ページが1つ以上あるか
```

という意味になります。

---

# 16. `context.new_page()`

```python
context.new_page()
```

新しいページ、つまり新しいタブを作ります。

戻り値は `Page` オブジェクトです。

```python
page = context.new_page()
```

以後は、この `page` を使ってWebページを操作します。

代表的な処理は次のとおりです。

```python
page.goto(...)
page.click(...)
page.fill(...)
page.screenshot(...)
```

---

# 17. `page` とは

`page` は、ブラウザの1つのタブを表すオブジェクトです。

例えば、次の処理ができます。

```python
page.goto("http://localhost:3000")
```

```python
page.screenshot(path="capture.png")
```

```python
page.locator("button").click()
```

```python
title = page.title()
```

今回のアプリでは、主に次の処理に使っています。

- Metabaseを開く
- URLを変更する
- 読み込みを待つ
- スクリーンショットを撮る

---

# 18. `page.goto()`

```python
page.goto(
    DASHBOARD_URL,
    wait_until="domcontentloaded",
    timeout=30_000,
)
```

`page.goto()` は、指定したURLを開くメソッドです。

一般的なブラウザ操作でいうと、アドレスバーへURLを入力してEnterキーを押す操作に相当します。

---

# 19. `DASHBOARD_URL`

```python
DASHBOARD_URL = "http://localhost:3000/dashboard/5"
```

これは開くページのURLです。

実際には、次のように呼び出されます。

```python
page.goto(
    "http://localhost:3000/dashboard/5",
    ...
)
```

MetabaseがローカルPCのポート3000番で動作していることを前提としています。

---

# 20. `wait_until="domcontentloaded"`

```python
wait_until="domcontentloaded",
```

これは、`page.goto()` がどの時点まで待つかを指定しています。

`domcontentloaded` は、HTMLの読み込みとDOMの構築が終わった時点です。

大まかな流れは次のとおりです。

```text
HTMLの受信開始
    ↓
HTML解析
    ↓
DOM作成完了
    ↓
DOMContentLoaded
    ↓
画像や追加通信が続くこともある
```

つまり、

```python
wait_until="domcontentloaded"
```

は、

> HTMLの基本構造が作られるまで待つ

という指定です。

---

## 20.1 DOMとは

DOMは、ブラウザがHTMLを扱うために作るオブジェクト構造です。

例えば次のHTMLがあるとします。

```html
<body>
    <h1>Metabase</h1>
    <button>更新</button>
</body>
```

ブラウザ内部では、概念的に次のような構造として扱われます。

```text
body
├── h1
└── button
```

この構造が作られた時点が `domcontentloaded` です。

---

## 20.2 Metabaseでは表示完了と同じではない

MetabaseはJavaScriptでグラフやカードを後から描画します。

そのため、

```text
DOMContentLoaded
```

になっても、グラフ描画が終わっていない場合があります。

だから元のプログラムでは、別の関数でさらに待っています。

```python
wait_for_dashboard(page)
```

その中では、

```python
page.wait_for_load_state("networkidle")
time.sleep(DRAW_WAIT_SECONDS)
```

のような待機を行っています。

これはMetabaseのような動的Webアプリでは重要です。

---

# 21. `timeout=30_000`

```python
timeout=30_000,
```

ページの読み込みを最大30秒待つ指定です。

Playwrightの時間指定は、基本的にミリ秒です。

```text
1秒 = 1,000ミリ秒
30秒 = 30,000ミリ秒
```

Pythonでは数字の途中に `_` を入れられます。

```python
30_000
```

と

```python
30000
```

は同じ値です。

`30_000` の方が、30,000であることを読み取りやすくなります。

---

## 21.1 タイムアウトした場合

30秒以内に指定した読み込み状態へ到達しない場合、Playwrightの `TimeoutError` が発生します。

元のコードでは、次のように名前を付け替えてimportしています。

```python
from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
)
```

そのため、例外処理では次のように書けます。

```python
except PlaywrightTimeoutError:
    print("ページ読込みがタイムアウトしました。")
```

---

# 22. ここまでの処理を日本語にする

コード全体を日本語へ置き換えると、次のようになります。

```text
同期版Playwrightを開始する

Google Chromeを、
Playwright専用のユーザーデータフォルダを使って起動する

ブラウザ画面は表示する

Webページ表示領域を1920×1080にする

すでにタブがあれば最初のタブを使う

タブがなければ新しいタブを作る

MetabaseのダッシュボードURLを開く

HTMLの基本構造が読み込まれるまで、
最大30秒待つ
```

---

# 23. 最小構成へ簡略化した例

細かな設定を外すと、次のように書けます。

```python
from playwright.sync_api import sync_playwright


with sync_playwright() as playwright:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir="playwright_browser_data",
        channel="chrome",
        headless=False,
    )

    try:
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("http://localhost:3000")
    finally:
        context.close()
```

初心者が最初に覚えるなら、この形から始めてもよいでしょう。

---

# 24. 通常のブラウザ起動との違い

Playwrightには、次のような一般的な起動方法もあります。

```python
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(
        headless=False,
    )

    context = browser.new_context()
    page = context.new_page()

    page.goto("http://localhost:3000")

    browser.close()
```

この方法では、

```text
browser
    ↓
context
    ↓
page
```

を順番に作ります。

---

## 24.1 今回の方法

今回のコードでは、

```python
context = playwright.chromium.launch_persistent_context(...)
```

を使っています。

この方法は、

```text
Chrome起動
Browser Context作成
ユーザーデータ保存
```

をまとめて行います。

ログイン状態を維持したい今回の用途に適しています。

---

# 25. `launch()` と `launch_persistent_context()` の比較

| 項目 | `launch()` | `launch_persistent_context()` |
|---|---|---|
| Browserを返す | はい | いいえ |
| Contextを返す | いいえ | はい |
| ユーザーデータ保存 | 通常は一時的 | 指定フォルダへ保存 |
| ログイン状態維持 | 工夫が必要 | しやすい |
| 今回の用途 | やや不向き | 適している |

今回のアプリでは、Metabaseへ一度ログインした状態を次回も利用したいため、`launch_persistent_context()` が使われています。

---

# 26. 初心者がまず覚えるPlaywright操作

Playwrightを学び始めるときは、次の操作を順番に覚えると分かりやすいです。

## 26.1 ページを開く

```python
page.goto("http://localhost:3000")
```

## 26.2 要素を取得する

```python
button = page.locator("button")
```

## 26.3 クリックする

```python
button.click()
```

## 26.4 文字を入力する

```python
page.locator("input").fill("123")
```

## 26.5 スクリーンショットを保存する

```python
page.screenshot(
    path="capture.png",
    full_page=True,
)
```

## 26.6 読み込みを待つ

```python
page.wait_for_load_state("domcontentloaded")
```

---

# 27. 今回のアプリでPlaywrightが担当する範囲

今回のスクリーンショットアプリでは、Playwrightが次の仕事を担当しています。

```text
Chromeの起動
    ↓
Metabaseを開く
    ↓
URLパラメータを変更する
    ↓
ページの読み込みを待つ
    ↓
スクリーンショットを保存する
    ↓
Chromeを閉じる
```

一方、設備番号の一覧や保存ファイル名は、通常のPythonコードが担当します。

```python
for machine_no in MACHINE_NUMBERS:
    ...
```

```python
output_path = (
    pictures_directory
    / f"OpeGraph_MC{machine_no:03d}.png"
)
```

Playwrightは「ブラウザ操作担当」と考えると分かりやすいです。

---

# 28. よくあるエラー

## 28.1 Metabaseが起動していない

```text
http://localhost:3000
```

へ接続できないため、`page.goto()` が失敗します。

対策:

```text
先にMetabaseを起動する
```

---

## 28.2 Google Chromeが見つからない

```python
channel="chrome"
```

を指定しているため、Google Chromeがインストールされていないと起動できません。

---

## 28.3 プロファイルフォルダが競合する

同じ `playwright_browser_data` を使うChromeがすでに起動していると、起動できない場合があります。

対策:

```text
同じアプリを二重起動しない
```

---

## 28.4 読み込みは終わったがグラフが出ていない

`domcontentloaded` は、Metabaseのグラフ描画完了を保証しません。

対策:

```python
page.wait_for_load_state("networkidle")
time.sleep(DRAW_WAIT_SECONDS)
```

のように追加で待機します。

---

## 28.5 ブラウザが閉じられない

途中で例外が発生すると、終了処理が実行されない可能性があります。

対策として、

```python
try:
    ...
finally:
    context.close()
```

を使います。

---

# 29. 今回のコードの良い点

今回のコードには、初心者が参考にできる良い設計が多くあります。

- 同期APIを使っており、上から順に読める
- Google Chromeを明示している
- Playwright専用プロファイルを使っている
- ログイン状態を保持できる
- viewportを固定している
- 既存ページを再利用している
- タイムアウトを指定している
- `finally` で確実にブラウザを閉じている

特に、

```python
try:
    ...
finally:
    context.close()
```

は、安定した自動化プログラムを作るうえで重要です。

---

# 30. 全体まとめ

今回の中心コードは次のとおりです。

```python
with sync_playwright() as playwright:
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=browser_data_directory,
        channel="chrome",
        headless=False,
        viewport={
            "width": VIEWPORT_WIDTH,
            "height": VIEWPORT_HEIGHT,
        },
        ignore_default_args=[
            "--no-sandbox",
        ],
    )

    try:
        page = context.pages[0] if context.pages else context.new_page()

        page.goto(
            DASHBOARD_URL,
            wait_until="domcontentloaded",
            timeout=30_000,
        )
    finally:
        context.close()
```

このコードの意味を一文でまとめると、

> Playwrightを開始し、専用プロファイルを使ってGoogle Chromeを表示状態で起動し、既存または新規のタブでMetabaseを開き、処理終了時にChromeを閉じる。

となります。

初心者が最初に押さえるべき関係は次のとおりです。

```text
sync_playwright()
    ↓
Playwright開始

playwright.chromium
    ↓
Chromium系ブラウザを操作

launch_persistent_context()
    ↓
ログイン状態を保存できるChrome環境を起動

context.pages / context.new_page()
    ↓
タブを取得または作成

page.goto()
    ↓
URLを開く

context.close()
    ↓
ブラウザを閉じる
```

この流れを理解できれば、Playwrightによるブラウザ自動化の基礎はしっかり押さえられています。
