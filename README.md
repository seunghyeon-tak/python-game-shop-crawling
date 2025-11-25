# shop-crawler

> 앞으로 계속해서 업데이트 해 나아갈 예정

## 소개

현재 : 

> 웹 페이지의 형태로 된 게임 아이템 거래소를 기준으로 아이템 목록 / 개별 데이터를 수집하여 시세 분석과 인기매물 판단을 자동화 하는 파이썬 크롤러 입니다.

제안 :

> 웹 기반 게임 아이템 거래소(ex. mapleland.gg)를 대상으로, 아이템 목록과 개별 거래 데이터를 수집하여 시세 분석과 인기 매물 판단을 자동화 하는 파이썬 크롤러 입니다.

## 크롤러 사용한 방법

현재 : 

> HTML 파싱 대신 공개된 API를 사용함
> 서비스 구조를 변경에 비교적 덜 민감하고, 불필요한 트래픽을 줄이는 것을 목표로 한다.

## 주요 기능

- 아이템별 거래 내역 크롤링 및 시세 데이터 수집
- 수집된 데이터를 기반으로 한 아이템별 시세 분석
- 최근 거래량, 판매 상태, 판매자 수 등을 활용한 인기 매물(Hot, Moderate, Quiet 등) 판단 로직

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

- `src/crawler/items.py`
  - 공개 API(`/api/items`)에서 전체 아이템 목록을 가져오고 `itemCode`, `itemName` 등을 파싱한다.

- `src/crawler/trades.py`
  - 개별 아이템 코드 기준으로 거래 내역 API(`/trade?itemCode=...`)를 호출해 원시 거래 데이터를 수집합니다.

- `src/crawler/runner.py`
  - 아이템 목록을 순회하면서 각 아이템의 거래 내역을 수집하는 배치 크롤러 엔트리 포인트입니다.  
  - 요청 사이에 딜레이를 넣어 서비스에 부담을 줄이도록 설계되어 있습니다.

- `src/storage/file_storage.py`
  - 수집한 거래 데이터를 `data/` 디렉터리에 NDJSON 형태로 저장합니다.

- `src/analysis/popularity.py`
  - 최근 거래 수, 판매 상태 비율, 판매자 수 등을 기준으로 아이템별 “인기 매물” 여부를 계산합니다.


## 폴더 구조

```bash
shop-crawler/
│
├─ .gitignore
├─ README.md
├─ requirements.txt
├─ .env
│
├─ src/
│  ├─ main.py                # 전체 실행 진입점 (기존 run_collect.py 역할)  
│  ├─ data/                     # 크롤링 결과 저장 (NDJSON/CSV 등)
│  │
│  ├─ crawler/               # 크롤링 관련 모듈
│  │  ├─ __init__.py
│  │  ├─ items.py            # 아이템 목록 수집(fetch_items)
│  │  ├─ trades.py           # 거래 내역 수집(fetch_trades)
│  │  ├─ runner.py           # crawl_all / 배치 수집 로직
│  │  └─ http_client.py      # 재시도/백오프 포함 요청 유틸
│  │
│  ├─ storage/               # 저장/DB 관련 모듈
│  │  ├─ __init__.py
│  │  ├─ file_storage.py     # NDJSON/CSV 저장
│  │  └─ db_storage.py       # (다음 단계) DB 연결/적재
│  │
│  ├─ analysis/              # 분석/통계 관련 모듈
│  │  ├─ __init__.py
│  │  └─ popularity.py       # 인기도 계산
│  │
│  └─ utils/                 # 공통 유틸리티
│     └─ __init__.py
```

## 실행 방법

프로젝트 루트에서 가상환경(.venv)을 활성화한 뒤, 아래 명령으로 전체 크롤링 파이프라인을 실행할 수 있습니다.

```bash
cd shop-crawler

python -m src.main
```