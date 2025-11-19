import datetime
import hashlib
import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)


def dedup_key(t: dict) -> str:
    raw = f"{t.get('url')} | {t.get('itemCode')} | {t.get('created_at')} | {t.get('itemPrice')}"
    return hashlib.sha1(raw.encode()).hexdigest()


def save_trades(trades: list):
    day = datetime.date.today().isoformat()
    path = os.path.join(DATA_DIR, f"trades_{day}.ndjson")

    seen = set()

    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    if "_k" in obj:
                        seen.add(obj["_k"])
                except:
                    pass

    with open(path, "a", encoding="utf-8") as f:
        for t in trades:
            k = dedup_key(t)
            if k in seen:
                continue
            out = {"_k": k, **{k2: t.get(k2) for k2 in (
                "itemCode", "itemName", "itemPrice", "tradeStatus", "created_at"
            )}, "raw": t}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
