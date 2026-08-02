import re
import time
from pathlib import Path

from playwright.sync_api import (
    Page,
    TimeoutError as PlaywrightTimeoutError,
    sync_playwright,
)


# ============================================================
# ユーザー設定
# ============================================================

# 撮影対象の設備番号
MACHINE_NUMBERS = [
    # 第1工場
    1, 3, 4, 6, 7, 10, 12, 13, 14, 17, 30, 32, 40,

    # 第3工場
    18, 36, 46, 47, 48, 49, 50,

    # 第4工場 1F
    34, 35, 43, 63, 41, 44, 45, 57,

    # 第4工場 2F
    39, 42, 52, 53, 54, 64,
]

# 対象ダッシュボード
DASHBOARD_URL = "http://localhost:3000/dashboard/5"

# Metabaseのグラフ描画を待つ秒数
DRAW_WAIT_SECONDS = 3

# ブラウザ表示サイズ (Full HD)
VIEWPORT_WIDTH = 1920
VIEWPORT_HEIGHT = 1080


# ============================================================
# 内部処理
# ============================================================
def get_pictures_directory() -> Path:
    """Windows標準の「ピクチャ」フォルダを取得する。"""
    pictures_directory = Path.home() / "Pictures"

    pictures_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return pictures_directory


def set_machine_no(url: str, machine_no: int) -> str:
    """URL内のmachine_noを置換する。存在しない場合は末尾へ追加する。"""
    # (Referenceフォルダ内の解説書参照のこと)
    pattern = re.compile(r"([?&])machine_no=[^&#]*")

    if pattern.search(url):
        return pattern.sub(
            lambda match: f"{match.group(1)}machine_no={machine_no}",
            url,
            count=1,
        )

    separator = "&" if "?" in url else "?"
    return f"{url}{separator}machine_no={machine_no}"


def wait_for_dashboard(page: Page) -> None:
    """ページ読込みとグラフ描画を待つ。"""
    page.wait_for_load_state("domcontentloaded")

    # Metabaseは通信が継続する場合があるため、networkidleだけに依存しない。
    try:
        page.wait_for_load_state(
            "networkidle",
            timeout=10_000,
        )
    except PlaywrightTimeoutError:
        pass

    time.sleep(DRAW_WAIT_SECONDS)


def main() -> None:
    """設備番号を切り替え、ダッシュボード全体をPNG保存する。"""
    pictures_directory = get_pictures_directory()

    app_directory = Path(__file__).resolve().parent
    browser_data_directory = app_directory / "playwright_browser_data"

    print("=" * 68)
    print(" Metabase 設備別スクリーンショット")
    print("=" * 68)
    print(f"保存先: {pictures_directory}")
    print(
        "対象設備: "
        + ", ".join(str(number) for number in MACHINE_NUMBERS)
    )
    print()

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

            print()
            print("【手動操作】")
            print("1. 必要ならMetabaseへログインしてください。")
            print("2. 日付フィルターを設定してください。")
            print("3. ダッシュボードの表示を確認してください。")
            input("準備ができたらEnterキーを押してください。")


            # 手動設定後のURLを基準にする。
            # base_url = page.url     # これでは最新URL取得できなかった(Reference参照)
            base_url = page.evaluate("window.location.href")
            print(f"base_url={base_url}")


            print()
            print("スクリーンショットを開始します。")

            for machine_no in MACHINE_NUMBERS:
                target_url = set_machine_no(base_url, machine_no)

                print(
                    f"Machine No. {machine_no}: "
                    "ダッシュボードを読み込んでいます..."
                )

                page.goto(
                    target_url,
                    wait_until="domcontentloaded",
                    timeout=30_000,
                )

                wait_for_dashboard(page)

                output_path = (
                    pictures_directory
                    / f"OpeGraph_MC{machine_no:03d}.png"
                )

                page.screenshot(
                    path=str(output_path),
                    full_page=True,
                )

                print(f"保存完了: {output_path.name}")

            print()
            print("すべてのスクリーンショットを保存しました。")
            print(f"保存先: {pictures_directory}")

        finally:
            context.close()


if __name__ == "__main__":
    main()



