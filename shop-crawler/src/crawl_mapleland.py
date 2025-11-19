import os
import time

from dotenv import load_dotenv

from fetch_items import fetch_items
from fetch_trades import fetch_trades

load_dotenv()

PER_REQUEST_DELAY = float(os.getenv("PER_REQUEST_DELAY", "1.0"))
BATCH_DELAY = float(os.getenv("BATCH_DELAY", "5.0"))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))


def iter_chunks(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i:i + n]


def crawl_all():
    items = fetch_items()
    for group in iter_chunks(items, BATCH_SIZE):
        for it in group:
            trades = fetch_trades(it["itemCode"])
            yield it, trades
            time.sleep(PER_REQUEST_DELAY)
        time.sleep(BATCH_DELAY)


if __name__ == "__main__":
    for meta, trades in crawl_all():
        print(meta, "건수 : ", len(trades))
        break
