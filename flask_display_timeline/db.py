import sqlite3
import struct
from pathlib import Path


DB_PATH = Path(
    r"\\192.168.2.1\共有ファイル\M-光和共有ファイル\P_ProductControl"
    r"\operation_data\main_factory_production_data.db"  
)


def get_all_data(
        machine_no: int,
        production_date: str,
) -> list[int]:
    """指定設備・指定生産日のall_data(BLOB)をuint16リストとして取得する。"""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT all_data
            FROM operation_data
            WHERE machine_no = ?
              AND production_date = ?
            """,
            (machine_no, production_date)
        )

        row = cursor.fetchone()

    if row is None:
        raise ValueError(
            "指定した設備・生産日のデータがありません。"
            f"machine_no={machine_no}, production_date={production_date}"
        )

    blob = row[0]

    if blob is None:
        raise ValueError(
            "all_dataが空です。"
            f"machine_no={machine_no}, production_date={production_date}"
        )

    count = len(blob) // 2    
    values = list(struct.unpack(f"<{count}H", blob))

    if len(values) != 1500:
        raise ValueError(
            f"all_data の数が不正です。期待値=1500、実際={len(values)}"
        )

    return values