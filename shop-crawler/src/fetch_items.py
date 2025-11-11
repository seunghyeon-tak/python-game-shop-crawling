import os
from dotenv import load_dotenv
from http_client import get_json

load_dotenv()

BASE = os.getenv("MAPLELAND_BASE_URL")

def fetch_items():
    items = get_json(BASE)

    return [{"itemCode": it["itemCode"], "itemName": it["itemName"]} for it in items]

if __name__ == "__main__":
    data = fetch_items()
    print(f"아이템 개수 : {len(data)}")
    print("샘플 : ", data[:3])