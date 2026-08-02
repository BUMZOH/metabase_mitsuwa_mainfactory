# `set_machine_no()` 関数 詳細解説（前編）

作成日: 2026-08-02

---

## 1. はじめに

この資料では、次の `set_machine_no()` 関数を詳しく解説します。

```python
def set_machine_no(url: str, machine_no: int) -> str:
    """URL内のmachine_noを置換する。存在しない場合は末尾へ追加する。"""
    pattern = re.compile(r"([?&])machine_no=[^&#]*")

    if pattern.search(url):
        return pattern.sub(
            lambda match: f"{match.group(1)}machine_no={machine_no}",
            url,
            count=1,
        )

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}machine_no={machine_no}"
```

この関数の目的は、URL内にある `machine_no` パラメータの値を変更することです。

URLにすでに `machine_no` が存在する場合は、その部分を置換します。

URLに `machine_no` が存在しない場合は、URLの末尾に新しく追加します。

---

## 2. この関数が必要な理由

今回のアプリでは、Metabaseのダッシュボードを設備番号ごとに切り替えて表示します。

例えば、次のURLがあるとします。

```text
http://localhost:3000/dashboard/5?machine_no=1
```

このURLの設備番号を `3` に変更したい場合、次のURLを作る必要があります。

```text
http://localhost:3000/dashboard/5?machine_no=3
```

さらに、URLに `machine_no` がまだ存在しない場合もあります。

```text
http://localhost:3000/dashboard/5
```

この場合は、次のように新しく追加します。

```text
http://localhost:3000/dashboard/5?machine_no=3
```

つまり、この関数は次の2つの処理を担当します。

```text
machine_no が存在する
    ↓
既存の値を置換する

machine_no が存在しない
    ↓
新しく追加する
```

---

## 3. URLの基本構造

この関数を理解するためには、URLのクエリパラメータについて知る必要があります。

次のURLを例にします。

```text
http://localhost:3000/dashboard/5?machine_no=3
```

このURLは、大きく次の2つに分かれます。

```text
http://localhost:3000/dashboard/5
```

これは、表示するページのURLです。

```text
?machine_no=3
```

これは、ページへ渡す追加情報です。

このような追加情報を、一般に **クエリパラメータ** と呼びます。

---

## 4. `?` と `&` の役割

URLに最初のクエリパラメータを追加するときは、`?` を使います。

```text
http://localhost:3000/dashboard/5?machine_no=3
```

複数のクエリパラメータを追加するときは、2個目以降を `&` でつなぎます。

```text
http://localhost:3000/dashboard/5?date=2026-08-02&machine_no=3
```

整理すると、次のようになります。

```text
最初のパラメータ   → ?
2個目以降          → &
```

この違いがあるため、`machine_no` の直前は `?` の場合もあれば、`&` の場合もあります。

---

## 5. 関数宣言の解説

```python
def set_machine_no(url: str, machine_no: int) -> str:
```

### 5.1 関数名

```python
set_machine_no
```

意味は、「設備番号を設定する」です。

### 5.2 `url: str`

`url` という引数には文字列を渡します。

```python
url = "http://localhost:3000/dashboard/5"
```

`str` は文字列型を表す型ヒントです。

### 5.3 `machine_no: int`

`machine_no` には設備番号を整数で渡します。

```python
machine_no = 3
```

`int` は整数型を表す型ヒントです。

### 5.4 `-> str`

この関数は、処理後のURLを文字列として返します。

---

## 6. docstringの解説

```python
"""URL内のmachine_noを置換する。存在しない場合は末尾へ追加する。"""
```

これはdocstringです。

この一文で、次の2つの処理が説明されています。

```text
machine_no がある場合   → 置換
machine_no がない場合   → 追加
```

---

## 7. `re` モジュールとは

この関数では、Python標準ライブラリの `re` モジュールを使用します。

```python
import re
```

`re` は、正規表現を扱うためのモジュールです。

正規表現は、文字列の中から特定のルールに一致する部分を検索したり、置換したりするときに使います。

---

## 8. 正規表現とは

通常の文字列検索では、決まった文字列を探します。

```python
"machine_no=" in url
```

しかし今回探したい文字列は、次のように複数の形があります。

```text
?machine_no=1
&machine_no=1
?machine_no=30
&machine_no=999
```

設備番号は毎回異なります。

また、`machine_no` の直前は `?` の場合もあれば、`&` の場合もあります。

正規表現を使うと、次のようなルールで検索できます。

```text
先頭は ? または &
その後に machine_no=
その後は & または # が現れるまで何文字でもよい
```

---

## 9. `re.compile()` の解説

```python
pattern = re.compile(r"([?&])machine_no=[^&#]*")
```

`re.compile()` は、正規表現の検索パターンを作ります。

作成した検索パターンは、変数 `pattern` に保存されます。

その後、次のような処理に利用できます。

```python
pattern.search(url)
pattern.sub(...)
```

---

## 10. Raw文字列 `r""`

正規表現は次のように書かれています。

```python
r"([?&])machine_no=[^&#]*"
```

先頭の `r` はRaw文字列を表します。

今回の正規表現ではバックスラッシュを使っていないため、`r` がなくても同じように動作します。

ただし、正規表現では次のようにバックスラッシュをよく使います。

```python
r"\d+"
r"\w+"
r"\s+"
```

そのため、正規表現は `r""` で書くというルールに統一すると分かりやすくなります。

---

## 11. 正規表現全体

今回の正規表現は次のとおりです。

```text
([?&])machine_no=[^&#]*
```

これを分解すると、次の4つに分かれます。

```text
([?&])
machine_no=
[^&#]
*
```

---

## 12. `[?&]` の意味

```text
[?&]
```

角括弧 `[]` は、「中に書かれた文字のどれか1文字」を表します。

今回の `[?&]` は、次のどちらか1文字に一致します。

```text
?
&
```

したがって、次のどちらにも対応できます。

```text
?machine_no=
&machine_no=
```

---

## 13. `()` の意味

```text
([?&])
```

丸括弧 `()` は、一致した部分を記憶するために使います。

この仕組みを **キャプチャ** と呼びます。

今回記憶するのは、`?` または `&` です。

後で次のコードを使って取り出します。

```python
match.group(1)
```

---

## 14. `machine_no=` の意味

```text
machine_no=
```

この部分は正規表現の特別な記号ではありません。

そのまま `machine_no=` という文字列に一致します。

---

## 15. `[^&#]` の意味

```text
[^&#]
```

角括弧の先頭にある `^` は、「中に書かれた文字以外」を意味します。

今回の `[^&#]` は、`&` と `#` 以外の1文字に一致します。

URLでは、`&` が次のクエリパラメータの開始を表します。

そのため、`machine_no` の値だけを取り出すために使われています。

---

## 16. `*` の意味

```text
*
```

アスタリスクは、「直前の条件を0回以上繰り返す」という意味です。

今回の

```text
[^&#]*
```

は、次の意味になります。

```text
& または # 以外の文字が0文字以上続く
```

例えば、次の値に一致します。

```text
1
3
30
999
```

---

## 17. 正規表現全体の意味

```text
([?&])machine_no=[^&#]*
```

全体では、次の意味になります。

```text
? または & から始まり、
machine_no= が続き、
その後は & または # が現れるまで文字が続く
```

一致する例:

```text
?machine_no=1
&machine_no=3
?machine_no=30
&machine_no=999
```

---

## 18. `pattern.search(url)` の解説

```python
if pattern.search(url):
```

`search()` は、文字列の中に正規表現と一致する部分があるか検索します。

一致する部分が見つかった場合はMatchオブジェクトを返します。

見つからなかった場合は `None` を返します。

したがって、この条件式は次の意味です。

```text
URL内に machine_no が存在する場合
```

---

## 19. `pattern.sub()` の役割

```python
return pattern.sub(
    lambda match: f"{match.group(1)}machine_no={machine_no}",
    url,
    count=1,
)
```

`sub()` は、正規表現に一致した部分を別の文字列へ置換します。

例えば、次の部分を

```text
?machine_no=1
```

次のように変更します。

```text
?machine_no=3
```

---

## 20. `sub()` の3つの指定

```python
pattern.sub(
    置換後の内容,
    検索対象の文字列,
    count=1,
)
```

今回のコードでは次の意味になります。

```text
第1引数 → 一致部分を何に置換するか
第2引数 → どの文字列を対象にするか
count=1 → 最初の1件だけ置換する
```

---

## 21. `lambda` の基礎

```python
lambda match: f"{match.group(1)}machine_no={machine_no}"
```

`lambda` は、短い関数をその場で作るための構文です。

通常の関数として書くと、次のようになります。

```python
def create_replacement(match):
    return f"{match.group(1)}machine_no={machine_no}"
```

これを短く書いたものが `lambda` です。

---

## 22. `match.group(1)` の意味

```python
match.group(1)
```

これは、1番目の丸括弧でキャプチャした部分を取得します。

今回の正規表現では、次の部分です。

```text
([?&])
```

そのため、結果は `?` または `&` になります。

---

## 23. なぜ `?` または `&` を残すのか

例えば、次のURLでは `?` が必要です。

```text
http://localhost:3000/dashboard/5?machine_no=3
```

次のURLでは `&` が必要です。

```text
http://localhost:3000/dashboard/5?date=2026-08-02&machine_no=3
```

そのため、元の `?` または `&` を `match.group(1)` で取り出し、置換後の文字列でも再利用します。

---

## 24. f文字列による置換文字列の作成

```python
f"{match.group(1)}machine_no={machine_no}"
```

例えば、`match.group(1)` が `?` で、`machine_no` が `3` の場合は次の文字列になります。

```text
?machine_no=3
```

`match.group(1)` が `&` の場合は次の文字列になります。

```text
&machine_no=3
```

---

## 25. `count=1` の意味

```python
count=1
```

これは、最初に一致した1か所だけを置換する指定です。

通常、URL内に同じ名前の `machine_no` が複数存在することは想定しません。

そのため、最初の1件だけを置換しています。

---

## 26. `return` による即時終了

```python
if pattern.search(url):
    return pattern.sub(...)
```

URLに `machine_no` が存在した場合、置換後のURLを返します。

`return` が実行されると、関数はそこで終了します。

そのため、後ろにある追加処理は実行されません。

---

## 27. 置換処理の具体例

### 例1: 最初のパラメータとして存在する場合

入力:

```text
http://localhost:3000/dashboard/5?machine_no=1
```

新しい設備番号:

```text
3
```

結果:

```text
http://localhost:3000/dashboard/5?machine_no=3
```

### 例2: 2個目のパラメータとして存在する場合

入力:

```text
http://localhost:3000/dashboard/5?date=2026-08-02&machine_no=1
```

新しい設備番号:

```text
3
```

結果:

```text
http://localhost:3000/dashboard/5?date=2026-08-02&machine_no=3
```

---

## 28. 前編のまとめ

この関数の前半では、URLに `machine_no` がすでに存在する場合の処理を行っています。

中心となるコードは次の部分です。

```python
pattern = re.compile(r"([?&])machine_no=[^&#]*")

if pattern.search(url):
    return pattern.sub(
        lambda match: f"{match.group(1)}machine_no={machine_no}",
        url,
        count=1,
    )
```

処理内容を日本語にすると、次のようになります。

```text
? または & で始まる machine_no パラメータを探す

見つかったら、
? または & を残したまま、
machine_no の値を新しい設備番号へ置き換える
```

前編で登場した主な知識は次のとおりです。

| 記述 | 意味 |
|---|---|
| `re.compile()` | 正規表現パターンを作る |
| `r""` | Raw文字列 |
| `[]` | 中のどれか1文字 |
| `[^...]` | 中に指定した文字以外 |
| `()` | 一致部分をキャプチャする |
| `*` | 0回以上の繰り返し |
| `search()` | 一致部分を検索する |
| `sub()` | 一致部分を置換する |
| `lambda` | 短い無名関数を作る |
| `match.group(1)` | 1番目のキャプチャを取得する |
| `count=1` | 最初の1件だけ置換する |

後編では、URLに `machine_no` が存在しない場合の追加処理、三項演算子、さまざまなURL変換例、注意点を詳しく解説します。
