# Playwright × Metabase 不具合調査メモ

**作成日:** 2026-08-02

------------------------------------------------------------------------

# 現象

手動で日付フィルターを設定した後、ブラウザのアドレスバーには次のURLが表示されていた。

``` text
http://localhost:3000/dashboard/5?%25E6%2597%25A5%25E4%25BB%2598=2026-07-01~2026-07-31&machine_no=3
```

しかし、プログラムでは

``` python
base_url = page.url
print(f"base_url={base_url}")
```

を実行すると、

``` text
base_url=http://localhost:3000/dashboard/5
```

となり、日付パラメータが取得できなかった。

その結果、自動キャプチャ時には

``` text
http://localhost:3000/dashboard/5?%25E6%2597%25A5%25E4%25BB%2598=&machine_no=3
```

となり、日付フィルターが解除されてしまった。

------------------------------------------------------------------------

# 調査手順

## 1. タブの確認

まず、複数タブを疑った。

``` python
for index, opened_page in enumerate(context.pages):
    print(f"[{index}] URL = {opened_page.url}")
```

結果

``` text
[0] URL = http://localhost:3000/dashboard/5
```

タブは1枚だけだった。

------------------------------------------------------------------------

## 2. page.url の確認

``` python
print(page.url)
```

結果

``` text
http://localhost:3000/dashboard/5
```

アドレスバーと一致しなかった。

------------------------------------------------------------------------

## 3. ブラウザ内部のURL確認

``` python
print(page.evaluate("window.location.href"))
print(page.evaluate("document.URL"))
```

結果

``` text
window.location.href =
http://localhost:3000/dashboard/5?%25E6%2597%25A5%25E4%25BB%2598=2026-07-01~2026-07-31&machine_no=3

document.URL =
http://localhost:3000/dashboard/5?%25E6%2597%25A5%25E4%25BB%2598=2026-07-01~2026-07-31&machine_no=3
```

こちらはアドレスバーと一致した。

------------------------------------------------------------------------

# 原因

MetabaseはSPA（Single Page Application）である。

画面遷移を伴わずJavaScriptがURLを書き換えるため、

``` python
page.url
```

が最新のURLへ更新されないケースがあった。

一方、

``` python
page.evaluate("window.location.href")
```

はブラウザ内部の現在URLを取得するため、最新状態を取得できた。

------------------------------------------------------------------------

# 修正内容

変更前

``` python
base_url = page.url
```

変更後

``` python
base_url = page.evaluate("window.location.href")
```

これにより日付パラメータを保持したまま設備番号だけを書き換えられるようになった。

------------------------------------------------------------------------

# 教訓

PlaywrightでSPA（Metabase、React、Vue、Angularなど）を扱う場合は、

``` python
page.url
```

だけを信用しない。

必要に応じて

``` python
page.evaluate("window.location.href")
```

または

``` python
page.evaluate("document.URL")
```

で実際のURLを取得する。

------------------------------------------------------------------------

# 今回の切り分け手順（重要）

1.  タブ一覧を表示する
2.  `page.url` を確認する
3.  `window.location.href` を確認する
4.  `document.URL` を確認する
5.  差異があるか比較する

この順番で調査すると、PlaywrightとSPA特有のURL問題を効率よく切り分けられる。
