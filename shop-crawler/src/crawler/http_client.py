import os
import random
import time

import requests

HEADERS = {"User-Agent": os.getenv("USER_AGENT", "ItemlyticsBot/1.0")}
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))


def get_json(url: str, max_retries: int = 3):
    """
    가끔 429, 5xx 에러가 나올때 잠깐 쉬고 다시 시도하기 위한 메서드
    GET -> json + 지수 백오프 재시도
    """
    backoff = 1.0
    for attempt in range(max_retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            if r.status_code in (429,) or 500 <= r.status_code < 600:
                raise requests.HTTPError(f"retryable status {r.status_code}")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == max_retries:
                raise
            time.sleep(backoff * random.uniform(0.5, 1.5))
            backoff *= 2
