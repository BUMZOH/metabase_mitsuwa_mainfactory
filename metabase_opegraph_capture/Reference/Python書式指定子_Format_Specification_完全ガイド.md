# Python書式指定子（Format Specification）完全ガイド

## はじめに

Pythonでは、数値や文字列を表示するときに、次のような指定を書くことがあります。

```python
machine_no = 7

file_name = f"OpeGraph_MC{machine_no:03d}.png"

print(file_name)
```

実行結果：

```text
OpeGraph_MC007.png
```

この中の

```python
:03d
```

が**書式指定子（Format Specification）**です。

書式指定子を使うと、次のような表示を簡単に作れます。

- 整数を3桁のゼロ埋めで表示する
- 小数点以下を2桁にそろえる
- 数値にカンマを付ける
- 文字列を右寄せ・左寄せ・中央寄せする
- パーセント表示にする
- 16進数や2進数で表示する
- 符号を必ず表示する

書式指定子は、ファイル名、ログ、帳票、画面表示、CSV出力など、実務で非常によく使います。

---

# 1. 最初に覚えるべき例

## 1.1 `03d`の意味

```python
machine_no = 7

text = f"{machine_no:03d}"

print(text)
```

実行結果：

```text
007
```

`03d`は、次の3つに分けて考えます。

```text
0  3  d
│  │  └─ decimal integer：10進整数として表示
│  └──── 表示幅を最低3文字にする
└─────── 足りない桁を0で埋める
```

つまり、

> 10進整数を、最低3桁になるように、左側を0で埋めて表示する

という意味です。

### 例

```python
for machine_no in [1, 7, 12, 123, 1234]:
    print(f"{machine_no:03d}")
```

実行結果：

```text
001
007
012
123
1234
```

注意点：

`3`は「必ず3桁に切り詰める」という意味ではありません。

値が3桁を超えている場合は、そのまま表示されます。

```python
number = 1234

print(f"{number:03d}")
```

実行結果：

```text
1234
```

---

# 2. f文字列の基本

Pythonでは、文字列の中に変数を埋め込む方法として、**f文字列（f-string）**がよく使われます。

```python
name = "田中"
age = 35

message = f"{name}さんは{age}歳です。"

print(message)
```

実行結果：

```text
田中さんは35歳です。
```

書式指定子を使う場合は、変数名の後ろにコロンを書きます。

```python
f"{変数名:書式指定子}"
```

例：

```python
number = 7

print(f"{number:03d}")
```

---

# 3. 書式指定子の基本構造

Pythonの書式指定子は、概ね次の構造になっています。

```text
[[fill]align][sign][z][#][0][width][grouping][.precision][type]
```

初心者のうちは、すべてを一度に覚える必要はありません。

特によく使う部分は次のとおりです。

```text
[埋め文字][配置][符号][0埋め][幅][桁区切り][.精度][型]
```

たとえば、

```python
f"{value:0>8.2f}"
```

は次のように読みます。

```text
0   >   8   .2   f
│   │   │    │   └─ 固定小数点形式
│   │   │    └──── 小数点以下2桁
│   │   └──────── 最低8文字幅
│   └──────────── 右寄せ
└──────────────── 埋め文字は0
```

ただし、整数のゼロ埋めでは、通常は次の短い書き方を使います。

```python
f"{value:08d}"
```

---

# 4. 整数の書式指定

## 4.1 10進整数 `d`

`d`は、整数を10進数として表示する指定です。

```python
number = 25

print(f"{number:d}")
```

実行結果：

```text
25
```

通常の表示と同じため、`d`だけを書くことはあまりありません。

```python
print(f"{number}")
print(f"{number:d}")
```

どちらも結果は同じです。

```text
25
25
```

`d`は、桁数指定やゼロ埋めと組み合わせると便利です。

---

## 4.2 表示幅を指定する

```python
number = 25

print(f"|{number:5d}|")
```

実行結果：

```text
|   25|
```

`5d`の意味は次のとおりです。

```text
5：最低5文字幅
d：10進整数
```

整数は標準で右寄せになります。

---

## 4.3 ゼロ埋めする

```python
number = 25

print(f"{number:05d}")
```

実行結果：

```text
00025
```

用途例：

```python
machine_no = 7
file_name = f"OpeGraph_MC{machine_no:03d}.png"

print(file_name)
```

実行結果：

```text
OpeGraph_MC007.png
```

設備番号や連番をファイル名に含める場合、ゼロ埋めすると並び順がきれいになります。

ゼロ埋めなし：

```text
MC1.png
MC10.png
MC100.png
MC2.png
```

ゼロ埋めあり：

```text
MC001.png
MC002.png
MC010.png
MC100.png
```

---

## 4.4 桁区切りカンマを付ける

```python
number = 123456789

print(f"{number:,d}")
```

実行結果：

```text
123,456,789
```

`d`は省略できます。

```python
print(f"{number:,}")
```

実行結果：

```text
123,456,789
```

金額や生産数など、大きな数値を表示するときに便利です。

```python
production_count = 1250000

print(f"生産数：{production_count:,}個")
```

実行結果：

```text
生産数：1,250,000個
```

---

## 4.5 符号を必ず表示する

```python
for number in [10, 0, -10]:
    print(f"{number:+d}")
```

実行結果：

```text
+10
+0
-10
```

増減値を表示するときに便利です。

```python
difference = 15

print(f"前日比：{difference:+d}")
```

実行結果：

```text
前日比：+15
```

---

## 4.6 正の数に空白を入れる

```python
for number in [10, 0, -10]:
    print(f"{number: d}")
```

実行結果：

```text
 10
 0
-10
```

正の数には空白、負の数にはマイナス記号が表示されます。

縦に並べたときに符号位置をそろえられます。

---

# 5. 小数の書式指定

## 5.1 固定小数点形式 `f`

```python
value = 12.3456

print(f"{value:f}")
```

実行結果：

```text
12.345600
```

`f`を指定すると、標準では小数点以下6桁になります。

---

## 5.2 小数点以下の桁数を指定する

```python
value = 12.3456

print(f"{value:.2f}")
```

実行結果：

```text
12.35
```

`.2f`の意味：

```text
.2：小数点以下2桁
f ：固定小数点形式
```

指定桁より後ろは四捨五入されます。

```python
value = 3.14159265

print(f"{value:.0f}")
print(f"{value:.1f}")
print(f"{value:.2f}")
print(f"{value:.3f}")
```

実行結果：

```text
3
3.1
3.14
3.142
```

---

## 5.3 小数に表示幅を指定する

```python
value = 12.3456

print(f"|{value:8.2f}|")
```

実行結果：

```text
|   12.35|
```

`8.2f`の意味：

```text
8 ：全体を最低8文字幅にする
.2：小数点以下2桁
f ：固定小数点形式
```

重要：

`8`は整数部分だけの幅ではありません。

次のすべてを含む全体幅です。

- 符号
- 整数部分
- 小数点
- 小数部分

---

## 5.4 小数をゼロ埋めする

```python
value = 12.3

print(f"{value:08.2f}")
```

実行結果：

```text
00012.30
```

`08.2f`の意味：

```text
0 ：左側を0で埋める
8 ：全体を最低8文字幅にする
.2：小数点以下2桁
f ：固定小数点形式
```

---

## 5.5 小数にカンマを付ける

```python
value = 1234567.891

print(f"{value:,.2f}")
```

実行結果：

```text
1,234,567.89
```

金額や集計値に非常によく使います。

```python
amount = 1234567.5

print(f"合計金額：{amount:,.0f}円")
```

実行結果：

```text
合計金額：1,234,568円
```

---

# 6. パーセント表示

`%`を指定すると、値を100倍してパーセント記号を付けます。

```python
rate = 0.856

print(f"{rate:%}")
```

実行結果：

```text
85.600000%
```

小数点以下の桁数も指定できます。

```python
rate = 0.856

print(f"{rate:.1%}")
```

実行結果：

```text
85.6%
```

例：

```python
actual = 462
target = 540

achievement_rate = actual / target

print(f"達成率：{achievement_rate:.1%}")
```

実行結果：

```text
達成率：85.6%
```

注意：

元の値がすでに85.6の場合に`%`を使うと、8560%になります。

```python
rate = 85.6

print(f"{rate:.1%}")
```

実行結果：

```text
8560.0%
```

`%`を使う場合、元の値は通常、次のような割合です。

```text
0.856 → 85.6%
```

---

# 7. 文字列の配置

文字列では、表示幅と配置を指定できます。

## 7.1 左寄せ `<`

```python
text = "Python"

print(f"|{text:<10}|")
```

実行結果：

```text
|Python    |
```

---

## 7.2 右寄せ `>`

```python
text = "Python"

print(f"|{text:>10}|")
```

実行結果：

```text
|    Python|
```

---

## 7.3 中央寄せ `^`

```python
text = "Python"

print(f"|{text:^10}|")
```

実行結果：

```text
|  Python  |
```

幅が奇数になる場合は、左右の余白が完全には同じにならないことがあります。

---

## 7.4 埋め文字を指定する

配置記号の前に1文字を書くと、その文字で余白を埋められます。

```python
text = "Python"

print(f"{text:-<15}")
print(f"{text:->15}")
print(f"{text:-^15}")
```

実行結果：

```text
Python---------
---------Python
----Python-----
```

構造：

```text
-  ^
│  └─ 中央寄せ
└──── 埋め文字
```

見出しの作成にも使えます。

```python
title = "処理結果"

print(f" {title} ":=^40)
```

この書き方は構文エラーになるため、f文字列の中に書きます。

```python
title = "処理結果"

print(f"{f' {title} ':=^40}")
```

実行結果例：

```text
=============== 処理結果 ===============
```

より単純に書くなら、次でも構いません。

```python
title = " 処理結果 "

print(title.center(40, "="))
```

---

# 8. 数値の配置

数値は標準で右寄せです。

```python
for number in [1, 12, 123]:
    print(f"|{number:5d}|")
```

実行結果：

```text
|    1|
|   12|
|  123|
```

明示的に配置も指定できます。

```python
number = 123

print(f"|{number:<8d}|")
print(f"|{number:>8d}|")
print(f"|{number:^8d}|")
```

実行結果：

```text
|123     |
|     123|
|  123   |
```

---

# 9. `=`配置

`=`は数値専用に近い配置指定です。

符号を左端に残し、その後ろを埋めます。

```python
number = -123

print(f"{number:0=8d}")
```

実行結果：

```text
-0000123
```

比較：

```python
number = -123

print(f"{number:08d}")
print(f"{number:0=8d}")
```

実行結果：

```text
-0000123
-0000123
```

通常のゼロ埋めでは`08d`で十分です。

`=`は、符号と数値本体の間を特定文字で埋めたい場合に使えます。

```python
number = -123

print(f"{number:_=8d}")
```

実行結果：

```text
-____123
```

---

# 10. 2進数・8進数・16進数

## 10.1 2進数 `b`

```python
number = 10

print(f"{number:b}")
```

実行結果：

```text
1010
```

8桁のゼロ埋め：

```python
print(f"{number:08b}")
```

実行結果：

```text
00001010
```

---

## 10.2 8進数 `o`

```python
number = 10

print(f"{number:o}")
```

実行結果：

```text
12
```

---

## 10.3 16進数 `x` / `X`

小文字：

```python
number = 255

print(f"{number:x}")
```

実行結果：

```text
ff
```

大文字：

```python
print(f"{number:X}")
```

実行結果：

```text
FF
```

4桁ゼロ埋め：

```python
print(f"{number:04X}")
```

実行結果：

```text
00FF
```

PLC、通信データ、ビット演算、色コードなどで使うことがあります。

---

# 11. 基数の接頭辞を付ける `#`

`#`を付けると、2進数・8進数・16進数の接頭辞を表示できます。

```python
number = 255

print(f"{number:#b}")
print(f"{number:#o}")
print(f"{number:#x}")
print(f"{number:#X}")
```

実行結果：

```text
0b11111111
0o377
0xff
0XFF
```

ゼロ埋めとも組み合わせられます。

```python
number = 15

print(f"{number:#010b}")
```

実行結果：

```text
0b00001111
```

全体幅には`0b`も含まれます。

---

# 12. 指数表記

## 12.1 小文字の指数表記 `e`

```python
value = 1234567.89

print(f"{value:e}")
```

実行結果：

```text
1.234568e+06
```

小数点以下の桁数を指定：

```python
print(f"{value:.2e}")
```

実行結果：

```text
1.23e+06
```

---

## 12.2 大文字の指数表記 `E`

```python
value = 1234567.89

print(f"{value:.2E}")
```

実行結果：

```text
1.23E+06
```

---

# 13. 一般形式 `g` / `G`

`g`は、値に応じて固定小数点形式または指数表記を自動選択します。

```python
values = [123.456, 0.0000123456, 123456789]

for value in values:
    print(f"{value:g}")
```

結果は値や有効桁数によって変わります。

`g`の精度は、小数点以下の桁数ではなく、基本的に**有効桁数**です。

```python
value = 123.456789

print(f"{value:.4g}")
```

実行結果：

```text
123.5
```

画面表示を明示的に統一したい場合は、通常`.2f`などのほうが分かりやすいです。

---

# 14. 文字列の最大長を指定する

文字列に対して`.数字`を書くと、最大文字数を指定できます。

```python
text = "Python Programming"

print(f"{text:.6}")
```

実行結果：

```text
Python
```

幅と組み合わせることもできます。

```python
text = "Python Programming"

print(f"|{text:>20.6}|")
```

実行結果：

```text
|              Python|
```

`.6`で最大6文字に切り詰め、その後、幅20文字で右寄せしています。

---

# 15. `format()`関数で使う

書式指定子はf文字列だけでなく、`format()`関数でも使えます。

```python
number = 7

text = format(number, "03d")

print(text)
```

実行結果：

```text
007
```

f文字列：

```python
text = f"{number:03d}"
```

`format()`関数：

```python
text = format(number, "03d")
```

どちらも同じ結果です。

変数として書式を持ちたい場合は、`format()`が分かりやすいことがあります。

```python
format_spec = "08.2f"
value = 12.3

print(format(value, format_spec))
```

実行結果：

```text
00012.30
```

---

# 16. `str.format()`で使う

古いPythonコードでは、次の形式もよく見かけます。

```python
machine_no = 7

text = "MC{:03d}".format(machine_no)

print(text)
```

実行結果：

```text
MC007
```

名前付き引数：

```python
text = "MC{machine_no:03d}".format(machine_no=7)

print(text)
```

実行結果：

```text
MC007
```

現在、新しくコードを書く場合は、通常f文字列が最も読みやすいです。

```python
text = f"MC{machine_no:03d}"
```

---

# 17. 動的に幅や精度を変える

幅や小数点以下の桁数を変数で指定できます。

## 17.1 幅を変数で指定

```python
number = 123
width = 8

print(f"{number:{width}d}")
```

実行結果：

```text
     123
```

---

## 17.2 精度を変数で指定

```python
value = 3.14159265
precision = 3

print(f"{value:.{precision}f}")
```

実行結果：

```text
3.142
```

---

## 17.3 幅と精度を両方変数で指定

```python
value = 3.14159265
width = 10
precision = 3

print(f"{value:{width}.{precision}f}")
```

実行結果：

```text
     3.142
```

最初は少し読みにくく見えますが、内側の波括弧が変数部分です。

```text
{value:{width}.{precision}f}
       └──幅──┘ └精度┘
```

---

# 18. 日付と時刻の書式指定

`datetime`オブジェクトもf文字列で書式指定できます。

```python
from datetime import datetime

now = datetime.now()

print(f"{now:%Y-%m-%d}")
```

実行結果例：

```text
2026-08-02
```

よく使う指定：

| 指定 | 意味 | 例 |
|---|---|---|
| `%Y` | 西暦4桁 | `2026` |
| `%m` | 月2桁 | `08` |
| `%d` | 日2桁 | `02` |
| `%H` | 時24時間表記 | `15` |
| `%M` | 分 | `13` |
| `%S` | 秒 | `45` |

ファイル名用：

```python
from datetime import datetime

now = datetime.now()

file_name = f"export_{now:%Y%m%d_%H%M%S}.csv"

print(file_name)
```

実行結果例：

```text
export_20260802_151345.csv
```

これは次の書き方と同じです。

```python
file_name = now.strftime("export_%Y%m%d_%H%M%S.csv")
```

---

# 19. デバッグ用の`=`

Python 3.8以降では、変数名と値を同時に表示できます。

```python
machine_no = 7

print(f"{machine_no=}")
```

実行結果：

```text
machine_no=7
```

書式指定子も組み合わせられます。

```python
machine_no = 7

print(f"{machine_no=:03d}")
```

実行結果：

```text
machine_no=007
```

小数：

```python
rate = 0.856

print(f"{rate=:.1%}")
```

実行結果：

```text
rate=85.6%
```

デバッグ時に非常に便利です。

---

# 20. `!s`・`!r`・`!a`

書式指定子の前に、変換指定を書くことがあります。

```text
!s
!r
!a
```

## 20.1 `!s`

`str()`で文字列化します。

```python
value = "Python\nGuide"

print(f"{value!s}")
```

改行が実際の改行として表示されます。

---

## 20.2 `!r`

`repr()`で表現します。

```python
value = "Python\nGuide"

print(f"{value!r}")
```

実行結果：

```text
'Python\nGuide'
```

改行やタブ、空白を確認したいデバッグ時に便利です。

```python
text = "  ABC  "

print(f"{text!r}")
```

実行結果：

```text
'  ABC  '
```

---

## 20.3 `!a`

`ascii()`で変換します。

```python
text = "設備"

print(f"{text!a}")
```

Unicodeエスケープ表現になります。

通常の業務コードでは、使用頻度は高くありません。

---

# 21. よく使う実務例

## 21.1 設備番号を3桁表示

```python
machine_no = 7

machine_name = f"MC{machine_no:03d}"

print(machine_name)
```

実行結果：

```text
MC007
```

---

## 21.2 画像ファイル名を作る

```python
from pathlib import Path

pictures_directory = Path("pictures")
machine_no = 7

output_path = (
    pictures_directory
    / f"OpeGraph_MC{machine_no:03d}.png"
)

print(output_path)
```

実行結果：

```text
pictures/OpeGraph_MC007.png
```

Windowsでは、表示上の区切り文字が`\`になる場合があります。

---

## 21.3 連番ファイル名

```python
for index in range(1, 6):
    file_name = f"result_{index:04d}.csv"
    print(file_name)
```

実行結果：

```text
result_0001.csv
result_0002.csv
result_0003.csv
result_0004.csv
result_0005.csv
```

---

## 21.4 金額表示

```python
amount = 1234567.8

print(f"{amount:,.0f}円")
```

実行結果：

```text
1,234,568円
```

---

## 21.5 稼働率表示

```python
operation_rate = 0.92345

print(f"稼働率：{operation_rate:.1%}")
```

実行結果：

```text
稼働率：92.3%
```

---

## 21.6 秒数を固定幅で表示

```python
elapsed_seconds = 3.4567

print(f"処理時間：{elapsed_seconds:8.3f}秒")
```

実行結果：

```text
処理時間：   3.457秒
```

---

## 21.7 前回との差を符号付きで表示

```python
difference = -12

print(f"前回差：{difference:+d}")
```

実行結果：

```text
前回差：-12
```

正の場合：

```python
difference = 12

print(f"前回差：{difference:+d}")
```

実行結果：

```text
前回差：+12
```

---

## 21.8 表形式の表示

```python
data = [
    ("MC001", 1250, 0.923),
    ("MC002", 980, 0.875),
    ("MC010", 15320, 0.961),
]

print(f"{'設備':<8} {'生産数':>10} {'達成率':>8}")
print("-" * 30)

for machine, production, rate in data:
    print(
        f"{machine:<8} "
        f"{production:>10,} "
        f"{rate:>8.1%}"
    )
```

実行結果例：

```text
設備            生産数      達成率
------------------------------
MC001         1,250    92.3%
MC002           980    87.5%
MC010        15,320    96.1%
```

日本語は、使用するフォントや全角文字の扱いによって、見た目が完全にはそろわない場合があります。

---

# 22. 型と書式指定子の組み合わせ

書式指定子には、対象となる型があります。

## 22.1 整数に`d`

```python
number = 7

print(f"{number:03d}")
```

正常です。

文字列に`d`を使うとエラーになります。

```python
number = "7"

print(f"{number:03d}")
```

エラー例：

```text
ValueError: Unknown format code 'd' for object of type 'str'
```

文字列を整数に変換します。

```python
number = "7"

print(f"{int(number):03d}")
```

実行結果：

```text
007
```

---

## 22.2 文字列に`f`

```python
value = "12.34"

print(f"{value:.2f}")
```

エラーになります。

数値へ変換します。

```python
value = "12.34"

print(f"{float(value):.2f}")
```

実行結果：

```text
12.34
```

---

# 23. ゼロ埋めと`zfill()`の違い

文字列には`zfill()`というメソッドもあります。

```python
text = "7"

print(text.zfill(3))
```

実行結果：

```text
007
```

数値の書式指定：

```python
number = 7

print(f"{number:03d}")
```

実行結果：

```text
007
```

使い分け：

- 元データが整数なら、`f"{number:03d}"`が自然
- 元データが文字列なら、`text.zfill(3)`も使える
- 数値として扱うべき値を、最初から文字列として管理しないほうが安全な場合が多い

符号付き文字列にも対応します。

```python
text = "-7"

print(text.zfill(3))
```

実行結果：

```text
-07
```

---

# 24. `round()`との違い

```python
value = 12.3456

rounded_value = round(value, 2)

print(rounded_value)
```

実行結果：

```text
12.35
```

書式指定：

```python
print(f"{value:.2f}")
```

実行結果：

```text
12.35
```

違い：

- `round()`は数値を丸めた結果を返す
- 書式指定は表示用の文字列を作る
- 元の数値自体は変化しない

```python
value = 12.3456
text = f"{value:.2f}"

print(value)
print(text)
print(type(value))
print(type(text))
```

実行結果：

```text
12.3456
12.35
<class 'float'>
<class 'str'>
```

表示だけ整えたい場合は、書式指定が適しています。

---

# 25. 桁幅は最低幅である

これは非常に重要です。

```python
number = 12345

print(f"{number:03d}")
```

実行結果：

```text
12345
```

`3`は最大幅ではなく、最低幅です。

同様に、

```python
text = "ABCDEFGHIJ"

print(f"|{text:5}|")
```

実行結果：

```text
|ABCDEFGHIJ|
```

長い値は切り詰められません。

文字列を最大文字数で切り詰めたい場合は、精度を使います。

```python
text = "ABCDEFGHIJ"

print(f"|{text:.5}|")
```

実行結果：

```text
|ABCDE|
```

---

# 26. 負の数とゼロ埋め

```python
number = -7

print(f"{number:03d}")
```

実行結果：

```text
-07
```

全体で3文字になります。

```text
-
0
7
```

4桁にすると次のようになります。

```python
print(f"{number:04d}")
```

実行結果：

```text
-007
```

符号も表示幅に含まれます。

---

# 27. よくある間違い

## 27.1 コロンを書き忘れる

誤り：

```python
f"{machine_no03d}"
```

正しい書き方：

```python
f"{machine_no:03d}"
```

---

## 27.2 数字の0と英字のOを間違える

正しい指定：

```python
03d
```

先頭は英字の`O`ではなく、数字の`0`です。

---

## 27.3 文字列に`d`を指定する

誤り：

```python
machine_no = "7"

print(f"{machine_no:03d}")
```

正しい例：

```python
print(f"{int(machine_no):03d}")
```

---

## 27.4 `.2f`を「全体2桁」と誤解する

```python
value = 123.456

print(f"{value:.2f}")
```

実行結果：

```text
123.46
```

`.2f`は全体2桁ではなく、小数点以下2桁です。

---

## 27.5 `%`表示の元値を間違える

```python
rate = 85.6

print(f"{rate:.1%}")
```

実行結果：

```text
8560.0%
```

85.6%と表示したい場合：

```python
rate = 0.856

print(f"{rate:.1%}")
```

---

## 27.6 表示幅を超えたら切れると思う

```python
number = 123456

print(f"{number:3d}")
```

実行結果：

```text
123456
```

幅指定は最低幅です。

---

# 28. よく使う書式指定子一覧

| 書式 | 意味 | 例 |
|---|---|---|
| `d` | 10進整数 | `123` |
| `03d` | 3桁ゼロ埋め整数 | `007` |
| `8d` | 最低8文字幅の整数 | `     123` |
| `,d` | カンマ付き整数 | `1,234` |
| `+d` | 符号付き整数 | `+123` |
| `f` | 固定小数点 | `12.340000` |
| `.2f` | 小数点以下2桁 | `12.34` |
| `8.2f` | 幅8、小数点以下2桁 | `   12.34` |
| `08.2f` | ゼロ埋め、幅8、小数2桁 | `00012.34` |
| `,.2f` | カンマ付き、小数2桁 | `1,234.56` |
| `.1%` | パーセント、小数1桁 | `85.6%` |
| `<10` | 10文字幅で左寄せ | `ABC       ` |
| `>10` | 10文字幅で右寄せ | `       ABC` |
| `^10` | 10文字幅で中央寄せ | `   ABC    ` |
| `b` | 2進数 | `1010` |
| `o` | 8進数 | `12` |
| `x` | 16進数・小文字 | `ff` |
| `X` | 16進数・大文字 | `FF` |
| `#x` | 接頭辞付き16進数 | `0xff` |
| `.3e` | 指数表記、小数3桁 | `1.235e+03` |
| `%Y%m%d` | 日付 | `20260802` |

---

# 29. 覚え方

## 29.1 `03d`

```text
0：ゼロで埋める
3：3桁
d：10進整数
```

覚え方：

> ゼロ・3桁・デシマル

---

## 29.2 `.2f`

```text
.2：小数点以下2桁
f ：floatの固定小数点表示
```

覚え方：

> 小数点以下2桁のフロート表示

厳密には`f`は「fixed-point」の意味として理解するほうが適切です。

---

## 29.3 `,.1%`

```text
, ：3桁区切り
.1：小数点以下1桁
% ：100倍してパーセント表示
```

---

# 30. 実務でまず覚える6種類

最初は、次の6種類を覚えれば十分です。

## 整数のゼロ埋め

```python
f"{number:03d}"
```

## 整数のカンマ区切り

```python
f"{number:,}"
```

## 小数点以下2桁

```python
f"{value:.2f}"
```

## カンマ付き小数

```python
f"{value:,.2f}"
```

## パーセント

```python
f"{rate:.1%}"
```

## 文字列の配置

```python
f"{text:<10}"
f"{text:>10}"
f"{text:^10}"
```

---

# 31. 早見用チートシート

```python
number = 7
value = 1234.5678
rate = 0.856
text = "Python"
```

```python
f"{number:03d}"       # 007
f"{number:5d}"        # "    7"
f"{number:+d}"        # +7
f"{number:b}"         # 111
f"{number:04X}"       # 0007

f"{value:.2f}"        # 1234.57
f"{value:10.2f}"      # "   1234.57"
f"{value:010.2f}"     # 0001234.57
f"{value:,.2f}"       # 1,234.57

f"{rate:.1%}"         # 85.6%

f"{text:<10}"         # "Python    "
f"{text:>10}"         # "    Python"
f"{text:^10}"         # "  Python  "
f"{text:-^10}"        # "--Python--"
```

---

# 32. 今回のコードを改めて読む

```python
output_path = (
    pictures_directory
    / f"OpeGraph_MC{machine_no:03d}.png"
)
```

順番に読むと、次の意味になります。

## `pictures_directory`

画像の保存先フォルダを表す`Path`オブジェクトです。

## `/`

`pathlib.Path`では、`/`演算子でフォルダとファイル名を連結できます。

```python
pictures_directory / file_name
```

## `f"..."`

f文字列です。

文字列の中に変数を埋め込めます。

## `{machine_no:03d}`

`machine_no`を、3桁のゼロ埋め整数として文字列にします。

```text
1   → 001
7   → 007
12  → 012
123 → 123
```

## 完成するファイル名

```python
machine_no = 7
```

の場合：

```text
OpeGraph_MC007.png
```

最終的に、

```text
ピクチャフォルダ\OpeGraph_MC007.png
```

のような保存先パスになります。

---

# 33. まとめ

Pythonの書式指定子は、値を「どのように文字列として表示するか」を指定する仕組みです。

今回の重要ポイントは次のとおりです。

```python
f"{machine_no:03d}"
```

```text
0：不足桁を0で埋める
3：最低3文字幅
d：10進整数
```

したがって、

```python
machine_no = 7
```

なら、

```text
007
```

になります。

書式指定子は、元の数値を変更するのではなく、表示用の文字列を作ります。

```python
machine_no = 7
formatted = f"{machine_no:03d}"

print(machine_no)
print(formatted)
print(type(machine_no))
print(type(formatted))
```

実行結果：

```text
7
007
<class 'int'>
<class 'str'>
```

実務では、まず次の書式を使えるようになると便利です。

```python
f"{number:03d}"     # ゼロ埋め整数
f"{number:,}"       # カンマ区切り
f"{value:.2f}"      # 小数点以下2桁
f"{value:,.2f}"     # カンマ付き小数
f"{rate:.1%}"       # パーセント
f"{text:^20}"       # 中央寄せ
```

特にファイル名の連番や設備番号では、

```python
f"{machine_no:03d}"
```

が頻繁に登場します。

「0で埋める・3桁・10進整数」と分解して読むと、忘れにくくなります。
