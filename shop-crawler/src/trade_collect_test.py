import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("MAPLELAND_BASE_URL")
TRADE_BASE = os.getenv("MAPLELAND_TRADE_URL")
HEADERS = {"User-Agent": "Mozilla/5.0"}


def test_trade_fetch_single_item():
    # 아이템 리스트 중 하나만 가져오기
    res = requests.get(BASE, headers=HEADERS, timeout=10)
    res.raise_for_status()
    items = res.json()
    first_item = items[0]

    print(f"테스트용 아이템 : {first_item}")

    # 해당 itemCode로 거래 데이터 요청
    item_code = first_item["itemCode"]
    url = f"{TRADE_BASE}?itemCode={item_code}"
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    trades = res.json()

    # 응답 구조 확인 (앞의 1개만)
    print(json.dumps(trades[:1], indent=2, ensure_ascii=False))

    # 검증
    assert isinstance(trades, list), "응답이 리스트 형태가 아닙니다."

    if trades:
        trade = trades[0]
        required_keys = ["itemCode", "itemName", "tradeType", "itemPrice"]
        for key in required_keys:
            assert key in trade, f"{key} 필드 누락됨"


if __name__ == "__main__":
    test_trade_fetch_single_item()
