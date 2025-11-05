# shop-crawler

> 앞으로 계속해서 업데이트 해 나아갈 예정

웹 페이지의 형태로된 게임 아이템 거래소를 기준으로 아이템 목록 / 개별 데이터를 수집하여 시세 분석과 인기매물 판단을 자동화하는 파이썬 크롤러입니다.

HTML 파싱 대신 공개된 API를 사용합니다.

## 주요 기능

- 아이템별 시세 조회

## 데이터 소스

- 아이템 목록: https://mapleland.gg/api/items?v={version}

- 거래 목록: https://api.mapleland.gg/trade?itemCode={item_code}

  (실제 파라미터/응답 스키마는 서비스 업데이트에 따라 변경될 수 있습니다.)

## 요구 사항

- python 3.12.8
- 의존성 : requests, python-dotenv

**설치**

```bash
pip install -r requirements.txt
```

## .env 형식

.env 파일은 프로젝트 루트(shop-crawler/.env)에 위치시킨다.

실제 값은 서비스 정책에 맞게 조정 필요

```
# 필수
MAPLELAND_BASE_URL=https://mapleland.gg/api/items?v=251031
MAPLELAND_TRADE_URL=https://api.mapleland.gg/trade
```

## 기능 정리

**src/item_index_crawl.py**

-> BASE에서 전체 아이템 JSON을 받아 itemCode 리스트만 뽑고 원본 인덱스를 파일로 저장(items_index.json) 해 둔다.
