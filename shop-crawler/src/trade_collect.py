import json
import os
import random
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3 import Retry

load_dotenv()

BASE = os.getenv("MAPLELAND_BASE_URL")
TRADE_BASE = os.getenv("MAPLELAND_TRADE_URL")
HEADERS = {"User-Agent": "Mozilla/5.0"}

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

INDEX_PATH = DATA_DIR / "items_index.json"

CHECKPOINT = DATA_DIR / "checkpoint.jsonl"


def build_session():
    """요청 세션"""
    s = requests.Session()
    s.headers.update(HEADERS)

    retries = Retry(
        total=5,
        backoff_factor=1.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False
    )
    s.mount("http://", HTTPAdapter(max_retries=retries))
    s.mount("https://", HTTPAdapter(max_retries=retries))

    return s


session = build_session()


def polite_sleep(i, base=0.35, burst_every=80, burst_sleep=3.0):
    """
    base : 기본대기
    burst_every : 일정 횟수마다 긴 휴식
    """
    time.sleep(base + random.random() * 0.15)
    if i > 0 and i % burst_every == 0:
        time.sleep(burst_sleep + random.random())


def load_or_build_index():
    """
    인덱스 로드
    items_index.json 파일이 있다면 재활용하기 (API 과다 호출 방지)
    없으면 한 번 호출해서 저장
    """
    if INDEX_PATH.exists():
        with INDEX_PATH.open(encoding="utf-8") as f:
            items = json.load(f)
    else:
        res = session.get(BASE, timeout=10)
        res.raise_for_status()
        items = res.json()

        with INDEX_PATH.open("w", encoding="utf-8") as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

    codes = [it.get("itemCode") for it in items if it.get("itemCode") is not None]
    codes = list(dict.fromkeys(codes))

    return codes


def fetch_trade_info(item_code: int):
    """거래 API 호출"""
    url = f"{TRADE_BASE}?itemCode={item_code}"
    res = session.get(url, timeout=10)
    res.raise_for_status()
    return res.json()


def append_ndjson(path: Path, obj: dict):
    """데이터 줄 단위로 기록"""
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def load_last_index():
    """마지막으로 처리한 itemCode 인덱스 기억"""
    if not CHECKPOINT.exists():
        return -1
    last = -1

    with CHECKPOINT.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                rec = json.loads(line)
                last = rec.get("last_index", last)
            except:
                pass
    return last


def save_last_index(idx: int):
    """매 아이템 처리 후 저장"""
    append_ndjson(
        CHECKPOINT,
        {"ts": datetime.now().isoformat(), "last_index": idx}
    )

def daily_out_path():
    today = datetime.now().strftime("%Y-%m-%d")
    return DATA_DIR / f"trades_{today}.ndjson"


def run_all(chunk_size: int = 200):
    codes = load_or_build_index()
    start_from = load_last_index() + 1
    if start_from > 0:
        print(f"[INFO] Resuming from index {start_from} / {len(codes)}")

    processed = 0
    out_path = daily_out_path()

    for i, code in enumerate(codes[start_from:], start=start_from):
        try:
            data = fetch_trade_info(code)

            for t in data:
                record = {
                    "itemCode": t.get("itemCode"),
                    "itemName": t.get("itemName"),
                    "tradeType": t.get("tradeType"),
                    "itemPrice": t.get("itemPrice"),
                    "created_at": t.get("created_at"),
                    "itemOption": t.get("itemOption"),
                    "fetched_at": datetime.now().isoformat()
                }
                append_ndjson(out_path, record)
            processed += 1
        except requests.HTTPError as e:
            print(f"[WARN] HTTP error for {code}: {e}")
        except Exception as e:
            print(f"[WARN] Unexpected for {code}: {e}")
        finally:
            save_last_index(i)
            polite_sleep(i)

        if processed % chunk_size == 0:
            time.sleep(5 + random.random() * 2)


if __name__ == "__main__":
    run_all(chunk_size=200)
