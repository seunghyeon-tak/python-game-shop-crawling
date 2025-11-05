import json
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

BASE = os.getenv("MAPLELAND_BASE_URL")
TRADE_BASE = os.getenv("MAPLELAND_TRADE_URL")
HEADERS = {"User-Agent": "Mozilla/5.0"}
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)


def get_all_item_codes():
    res = requests.get(BASE, headers=HEADERS, timeout=10)
    res.raise_for_status()
    items = res.json()

    codes = [it.get("itemCode") for it in items if it.get("itemCode") is not None]
    codes = list(dict.fromkeys(codes))

    with open(DATA_DIR / "items_index.json", "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

    return codes


if __name__ == "__main__":
    codes = get_all_item_codes()
    print(f"아이템 갯수 : {len(codes)}")
    print("앞에서 5개만 미리보기 : ", codes[:5])
