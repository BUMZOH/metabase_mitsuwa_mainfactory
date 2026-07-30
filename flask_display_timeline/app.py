import base64
from datetime import date
from io import BytesIO

from flask import Flask, render_template, request

from common_lib_mw import create_ope_graph
import db

app = Flask(__name__)

# ----- FUNCTIONS ----------------------------------------
def data_convert_to_sine(data_1500: list[int]) -> list[int]:
    """本社工場の1500個データを、既存グラフ関数用の3330個形式へ変換する。"""
    data_3330 = data_1500 + [0] * 1830

    data_3330[4] = data_1500[2]     # 生産数
    data_3330[5] = data_1500[3]     # 異常数
    data_3330[7] = data_1500[4]     # 目標数

    return data_3330


def image_to_base64(image) -> str:
    """Pillow画像を、HTMLに埋め込めるBase64文字列へ変換する。"""
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def parse_production_date_range(value: str) -> tuple[date, date]:
    """Metabaseの日付文字列を開始日・終了日に変換する。"""
    date_parts = value.split("~", 1)

    if len(date_parts) == 1:
        start_date_text = date_parts[0]
        end_date_text = date_parts[0]
    else:
        start_date_text, end_date_text = date_parts

    start_date = date.fromisoformat(start_date_text)
    end_date = date.fromisoformat(end_date_text)

    if start_date > end_date:
        raise ValueError("開始日は終了日以前にしてください。")

    return start_date, end_date


# ----- FLASK FUNCTIONS -----------------------------------
@app.route("/")
def index():
    """動作確認用トップページを表示する"""
    return render_template("index.html")

@app.route("/machine-detail")
def machine_detail():
    """指定設備・指定稼働日の設備状態タイムラインを表示する。"""
    machine_no_text = request.args.get("machine_no")
    production_date_text = request.args.get("production_date")

    # print(machine_no_text)
    # print(production_date_text)

    # 注意: HTTPステータスコード400 -> Bad Request
    if machine_no_text is None or production_date_text is None:
        return render_template(
            "machine_detail.html",
            error_message="machine_no と production_date を指定してください。",
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 400

    try:
        machine_no = int(machine_no_text)
    except ValueError:
        return render_template(
            "machine_detail.html",
            error_message="machine_no は整数で指定してください。",
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 400

    try:
        start_date, end_date = parse_production_date_range(
            production_date_text
        )
    except ValueError:
        return render_template(
            "machine_detail.html",
            error_message=(
                "production_date は YYYY-MM-DD または"
                "YYYY-MM-DD～YYYY-MM-DD の形式で指定してください。"
            ),
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 400

    # タイムラインは1日分の画像なので、複数日の範囲は受け付けない。
    if start_date != end_date:
        return render_template(
            "machine_detail.html",
            error_message=(
                "設備状態タイムラインは1日単位で表示します。"
                "開始日と終了日を同じ日に指定してください。"
            ),
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 400

    target_date = start_date.isoformat()

    # 注意: HTTPステータスコード404 -> Not Found
    try:
        operation_data_1500 = db.get_all_data(
            machine_no=machine_no,
            production_date=target_date,
        )
    except ValueError as error:
        return render_template(
            "machine_detail.html",
            error_message=str(error),
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 404

    operation_data_3330 = data_convert_to_sine(operation_data_1500)

    timeline_image = create_ope_graph.get_ope_graph(
        operation_data_3330,
        title=f"MC{machine_no} / {target_date}"
    )

    # 注意: HTTPステータスコード500 -> Internal Server Error
    if timeline_image is None:
        return render_template(
            "machine_detail.html",
            error_message="タイムライン画像の作成に失敗しました",
            machine_no=machine_no_text,
            production_date=production_date_text,
            timeline_image_base64=None,
        ), 500

    # 正常時
    return render_template(
        "machine_detail.html",
        error_message=None,
        machine_no=machine_no_text,
        production_date=production_date_text,
        timeline_image_base64=image_to_base64(timeline_image),   
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )