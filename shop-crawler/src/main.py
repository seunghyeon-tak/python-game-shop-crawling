from dotenv import load_dotenv

from crawler.runner import crawl_all
from analysis.popularity import judge_popularity
from storage.file_storage import save_trades

load_dotenv()


def main():
    for meta, trades in crawl_all():
        save_trades(trades)
        pop = judge_popularity(trades)
        print(f"[{meta['itemName']}({meta['itemCode']})] "
              f"{pop['label']} score={pop['score']} "
              f"(1h={pop['last_1h']}, sell%={pop['sell_through_48h_pct']}, sellers={pop['unique_sellers']})")


if __name__ == "__main__":
    main()
