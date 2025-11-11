import os

from dotenv import load_dotenv

from http_client import get_json

load_dotenv()

TRADE_BASE = os.getenv("MAPLELAND_TRADE_URL")


def fetch_trades(item_code: int):
    """단일 아이템 거래 목록 가져오기"""
    url = f"{TRADE_BASE}?itemCode={item_code}"
    return get_json(url)


if __name__ == "__main__":
    print(fetch_trades(1432010)[:1])
