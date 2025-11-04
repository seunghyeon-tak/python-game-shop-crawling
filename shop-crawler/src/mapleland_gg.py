import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("MAPLELAND_BASE_URL")
TRADE_BASE = os.getenv("MAPLELAND_TRADE_URL")
HEADERS = {"User-Agent": "Mozilla/5.0"}

res = requests.get(BASE, headers=HEADERS, timeout=10)
res.raise_for_status()

data = res.json()


def fetch_trade_info(item_code: int):
    url = f"{TRADE_BASE}?itemCode={item_code}"
    res = requests.get(url, headers=HEADERS, timeout=10)
    res.raise_for_status()
    return res.json()


if __name__ == "__main__":
    for item_code in [1432010]:  # itemCode
        data = fetch_trade_info(item_code)
        trade_list = [trade for trade in data if trade.get("tradeType") == "sell"]

        for trade in trade_list:
            code = trade.get("itemCode")
            name = trade.get("itemName")
            price = trade.get("itemPrice")
            item_option = trade.get("itemOption")
            created_at = trade.get("created_at")

            print(
                f"아이템 코드 : {code} | "
                f"아이템 명 : {name} | "
                f"가격 : {price} | "
                f"합산 럭 : {item_option.get('incLUK')} | "
                f"합산 공격력: {item_option.get('incPAD')} | "
                f"추가 옵션 정리 : {item_option.get('optionSummarize')} | "
                f"업그레이드 남은 횟수 : {item_option.get('upgrade')} | "
                f"아이템 등록시간 : {created_at}"
            )
