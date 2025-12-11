"""
Pyfrontier datasets module.

サンプルデータセットを提供します。
"""

import csv
from pathlib import Path

# 列名の日英対応
_COLUMN_NAMES = {
    "都道府県": "prefecture",
    "図書館数": "n_libraries",
    "専任職員数": "n_fulltime_staff",
    "非常勤職員数": "n_parttime_staff",
    "司書数": "n_librarians",
    "図書冊数": "n_books",
    "登録者数": "n_registered_users",
    "貸出冊数": "n_loans",
    "視聴覚資料貸出数": "n_av_loans",
    "レファレンスサービス実施件数": "n_reference_services",
    "読書会実施件数": "n_reading_events",
    "鑑賞会実施件数": "n_viewing_events",
    "SNS利用館数": "n_sns_libraries",
}

# 都道府県名の日英対応
_PREFECTURE_NAMES = {
    "北海道": "Hokkaido",
    "青森県": "Aomori",
    "岩手県": "Iwate",
    "宮城県": "Miyagi",
    "秋田県": "Akita",
    "山形県": "Yamagata",
    "福島県": "Fukushima",
    "茨城県": "Ibaraki",
    "栃木県": "Tochigi",
    "群馬県": "Gunma",
    "埼玉県": "Saitama",
    "千葉県": "Chiba",
    "東京都": "Tokyo",
    "神奈川県": "Kanagawa",
    "新潟県": "Niigata",
    "富山県": "Toyama",
    "石川県": "Ishikawa",
    "福井県": "Fukui",
    "山梨県": "Yamanashi",
    "長野県": "Nagano",
    "岐阜県": "Gifu",
    "静岡県": "Shizuoka",
    "愛知県": "Aichi",
    "三重県": "Mie",
    "滋賀県": "Shiga",
    "京都府": "Kyoto",
    "大阪府": "Osaka",
    "兵庫県": "Hyogo",
    "奈良県": "Nara",
    "和歌山県": "Wakayama",
    "鳥取県": "Tottori",
    "島根県": "Shimane",
    "岡山県": "Okayama",
    "広島県": "Hiroshima",
    "山口県": "Yamaguchi",
    "徳島県": "Tokushima",
    "香川県": "Kagawa",
    "愛媛県": "Ehime",
    "高知県": "Kochi",
    "福岡県": "Fukuoka",
    "佐賀県": "Saga",
    "長崎県": "Nagasaki",
    "熊本県": "Kumamoto",
    "大分県": "Oita",
    "宮崎県": "Miyazaki",
    "鹿児島県": "Kagoshima",
    "沖縄県": "Okinawa",
}


def load_library_data(as_dataframe: bool = False, lang: str = "ja"):
    """図書館データセットを読み込む。

    都道府県別の公共図書館統計データを返します。

    Parameters
    ----------
    as_dataframe : bool, default False
        Trueの場合、pandas DataFrameとして返します。
        pandasがインストールされていない場合はImportErrorが発生します。
    lang : str, default "ja"
        言語設定。"ja"で日本語、"en"で英語の列名・都道府県名を使用。

    Returns
    -------
    list[dict] or pandas.DataFrame
        as_dataframe=Falseの場合は辞書のリスト、
        as_dataframe=Trueの場合はDataFrame。

    Examples
    --------
    >>> from Pyfrontier.datasets import load_library_data

    # 日本語（デフォルト）
    >>> data = load_library_data()
    >>> len(data)
    47

    # 英語でDataFrameとして取得
    >>> df = load_library_data(as_dataframe=True, lang="en")
    >>> df.columns[0]
    'prefecture'
    """
    if lang not in ("ja", "en"):
        raise ValueError(f"lang must be 'ja' or 'en', got '{lang}'")

    data_path = Path(__file__).parent / "library_prefecture.csv"

    if as_dataframe:
        try:
            import pandas as pd
        except ImportError:
            raise ImportError(
                "pandas is required for as_dataframe=True. "
                "Install it with: pip install pandas"
            )
        df = pd.read_csv(data_path)
        if lang == "en":
            df = df.rename(columns=_COLUMN_NAMES)
            df["prefecture"] = df["prefecture"].map(_PREFECTURE_NAMES)
        return df

    with open(data_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    if lang == "en":
        data = [
            {_COLUMN_NAMES.get(k, k): v for k, v in row.items()} for row in data
        ]
        for row in data:
            if "prefecture" in row:
                row["prefecture"] = _PREFECTURE_NAMES.get(
                    row["prefecture"], row["prefecture"]
                )

    return data


def get_library_data_path() -> Path:
    """図書館データセットのファイルパスを返す。

    Returns
    -------
    Path
        CSVファイルへのパス。
    """
    return Path(__file__).parent / "library_prefecture.csv"


__all__ = ["load_library_data", "get_library_data_path"]
