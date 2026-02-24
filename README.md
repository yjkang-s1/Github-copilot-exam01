# 📅 D-Day Counter (D-Day 카운터)

> 중요한 날짜(시험, 여행, 생일 등)를 등록하면 **D-Day를 자동 계산**하고,  
> 터미널 대시보드 · REST API · Streamlit 웹 앱으로 시각화하는 올인원 도구입니다.

---

## 📌 목차

1. [프로젝트 설명](#1--프로젝트-설명)
2. [실행 방법](#2--실행-방법)
3. [핵심 로직 / API 설명](#3--핵심-로직--api-설명)
4. [실행 화면 캡쳐](#4--실행-화면-캡쳐)5. [추가 기능 구현 목록](#5--추가-기능-구현-목록)
---

## 1. 📋 프로젝트 설명

### 1.1 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | D-Day Counter |
| **목표** | 중요한 날짜를 등록 → D-Day 자동 계산 → 대시보드 표시 |
| **핵심 기능** | 이벤트 CRUD, D-Day 계산, 가까운 순 정렬, 터미널/웹 대시보드 |
| **예상 개발 시간** | 30분 ~ 1시간 |

### 1.2 기술 스택

| 카테고리 | 기술 | 용도 |
|----------|------|------|
| 코어 | `Python`, `datetime`, `json` | 날짜 연산, 데이터 직렬화 |
| 데이터 모델 | `Pydantic v2` | 스키마 정의, 유효성 검사 |
| 터미널 UI | `Rich` | 컬러 테이블, 패널, KPI 대시보드 |
| REST API | `FastAPI` + `Uvicorn` | RESTful 엔드포인트 서빙 |
| 웹 UI | `Streamlit` + `Plotly` | 인터랙티브 대시보드, 차트 |
| 테스트 | `pytest` + `httpx` | 단위/통합 테스트 (41개) |

### 1.3 프로젝트 구조

```
Github-copilot-exam01/
├── app/
│   ├── __init__.py          # 패키지 초기화
│   ├── models.py            # Pydantic 데이터 모델
│   ├── dday_core.py         # D-Day 계산 핵심 로직
│   ├── storage.py           # JSON 파일 기반 CRUD 저장소
│   ├── dashboard.py         # Rich 터미널 대시보드
│   └── api.py               # FastAPI REST API
├── tests/
│   ├── test_step1_core.py   # 핵심 로직 테스트 (13개)
│   ├── test_step2_models.py # 데이터 모델 테스트 (7개)
│   ├── test_step3_storage.py# 저장소 CRUD 테스트 (10개)
│   └── test_step4_api.py    # API 엔드포인트 테스트 (11개)
├── data/
│   └── events.json          # 이벤트 데이터 (자동 생성)
├── streamlit_app.py         # Streamlit 웹 대시보드
├── generate_sample_data.py  # 샘플 데이터 생성 스크립트
├── requirements.txt         # 의존성 목록
└── README.md
```

### 1.4 데이터 구조 설계

#### 이벤트 모델 (`DdayEvent`)

```python
class DdayEvent(BaseModel):
    id: str            # 고유 ID (uuid hex 8자)
    title: str         # 이벤트 제목 (1~100자)
    target_date: date  # 목표 날짜
    category: EventCategory  # 카테고리 (시험/여행/생일/기념일/업무/기타)
    memo: str | None   # 메모 (선택, 최대 200자)
    created_at: datetime  # 생성 시각 (자동)
```

#### 카테고리 열거형

| 값 | 레이블 | 값 | 레이블 |
|----|--------|----|--------|
| `EXAM` | 시험 | `ANNIVERSARY` | 기념일 |
| `TRAVEL` | 여행 | `WORK` | 업무 |
| `BIRTHDAY` | 생일 | `OTHER` | 기타 |

#### 응답 모델 (`DdayEventResponse`)

기본 이벤트 필드에 추가로 아래 계산 필드를 포함합니다:

| 필드 | 타입 | 설명 |
|------|------|------|
| `d_day` | `int` | 양수: 남은 일수, 0: 오늘, 음수: 지난 일수 |
| `d_day_label` | `str` | `"D-5"`, `"🎉 D-Day!"`, `"D+3 (지남)"` |
| `is_past` | `bool` | 과거 이벤트 여부 |

#### JSON 저장 형식 (`data/events.json`)

```json
[
  {
    "id": "a1b2c3d4",
    "title": "기말 시험",
    "target_date": "2026-06-15",
    "category": "시험",
    "memo": "3층 강의실",
    "created_at": "2026-02-24T10:30:00"
  }
]
```

---

## 2. 🚀 실행 방법

### 2.1 설치

```bash
# 저장소 클론 또는 디렉토리 이동
cd Github-copilot-exam01

# 가상환경 생성 (권장)
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# 의존성 설치
pip install -r requirements.txt
```

### 2.2 샘플 데이터 생성

```bash
python generate_sample_data.py
```

> `data/events.json`에 8개의 샘플 이벤트(미래 6개, 과거 1개, 오늘 1개)가 생성됩니다.

### 2.3 터미널 대시보드 실행 (Rich)

```bash
python -m app.dashboard
```

### 2.4 FastAPI 서버 실행

```bash
uvicorn app.api:app --reload --port 8000
```

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2.5 Streamlit 웹 앱 실행

```bash
streamlit run streamlit_app.py
```

- **기본 주소**: http://localhost:8502

### 2.6 테스트 실행

```bash
# 전체 테스트 (41개)
python -m pytest tests/ -v

# 단계별 테스트
python -m pytest tests/test_step1_core.py -v     # 핵심 로직 (13개)
python -m pytest tests/test_step2_models.py -v    # 데이터 모델 (7개)
python -m pytest tests/test_step3_storage.py -v   # 저장소 CRUD (10개)
python -m pytest tests/test_step4_api.py -v       # API 엔드포인트 (11개)
```

#### 테스트 결과 (41 passed ✅)

```
tests/test_step1_core.py   ... 13 passed   (D-Day 계산, 레이블 포맷, 정렬)
tests/test_step2_models.py ...  7 passed   (모델 유효성, 카테고리 열거형)
tests/test_step3_storage.py .. 10 passed   (CRUD, JSON 직렬화)
tests/test_step4_api.py    ... 11 passed   (엔드포인트 CRUD, 필터, 요약)
───────────────────────────────────────────
                  합계       41 passed in 1.19s ✅
```

---

## 3. ⚡ 핵심 로직 / API 설명

### 3.1 핵심 로직 (`app/dday_core.py`)

#### `calculate_dday(target_date, base_date=None) → int`

오늘(또는 지정 날짜) 기준으로 D-Day를 계산합니다.

```python
calculate_dday(date(2026, 3, 10), base_date=date(2026, 3, 1))  # → 9  (D-9)
calculate_dday(date(2026, 2, 20), base_date=date(2026, 2, 24))  # → -4 (D+4 지남)
calculate_dday(date.today())                                      # → 0  (D-Day!)
```

#### `format_dday_label(d_day) → str`

정수 D-Day 값을 사람이 읽기 쉬운 레이블로 변환합니다.

| 입력 | 출력 |
|------|------|
| `5` | `"D-5"` |
| `0` | `"🎉 D-Day!"` |
| `-3` | `"D+3 (지남)"` |

#### `sort_events_by_proximity(events, base_date=None) → List[DdayEventResponse]`

이벤트 목록을 오늘 기준 **가까운 순서**로 정렬합니다:
1. **미래 이벤트** → 남은 일수 오름차순 (가까운 것 먼저)
2. **과거 이벤트** → 지난 일수 오름차순 (최근 것 먼저)

### 3.2 데이터 저장소 (`app/storage.py`)

JSON 파일 기반 CRUD 저장소로, 아래 함수들을 제공합니다:

| 함수 | 설명 |
|------|------|
| `load_events(path)` | JSON 파일에서 이벤트 목록 로드 |
| `save_events(events, path)` | 이벤트 목록을 JSON 파일로 저장 |
| `add_event(payload, path)` | 새 이벤트 추가 (ID 자동 생성) |
| `get_event(event_id, path)` | ID로 단일 이벤트 조회 |
| `update_event(event_id, payload, path)` | 이벤트 수정 (ID 유지) |
| `delete_event(event_id, path)` | 이벤트 삭제 |

### 3.3 FastAPI REST API (`app/api.py`)

#### 엔드포인트 목록

| 메서드 | 경로 | 설명 | 상태코드 |
|--------|------|------|----------|
| `GET` | `/` | 서버 헬스 체크 | 200 |
| `GET` | `/events` | 전체 이벤트 조회 (D-Day 포함) | 200 |
| `GET` | `/events/{id}` | 단일 이벤트 조회 | 200 / 404 |
| `POST` | `/events` | 새 이벤트 등록 | 201 |
| `PUT` | `/events/{id}` | 이벤트 수정 | 200 / 404 |
| `DELETE` | `/events/{id}` | 이벤트 삭제 | 200 / 404 |
| `GET` | `/summary` | 대시보드 KPI 요약 | 200 |

#### 쿼리 파라미터 (`GET /events`)

| 파라미터 | 타입 | 기본값 | 설명 |
|----------|------|--------|------|
| `category` | `EventCategory` | `None` | 카테고리 필터 (시험, 여행 등) |
| `sort` | `bool` | `true` | 가까운 순 정렬 여부 |

#### 요청/응답 예시

**이벤트 생성**
```http
POST /events
Content-Type: application/json

{
  "title": "기말 시험",
  "target_date": "2026-06-15",
  "category": "시험",
  "memo": "3층 강의실"
}
```

```json
// → 201 Created
{
  "id": "a1b2c3d4",
  "title": "기말 시험",
  "target_date": "2026-06-15",
  "category": "시험",
  "memo": "3층 강의실",
  "created_at": "2026-02-24T10:30:00",
  "d_day": 111,
  "d_day_label": "D-111",
  "is_past": false
}
```

**대시보드 요약**
```http
GET /summary
```

```json
{
  "total": 8,
  "upcoming": 6,
  "past": 2,
  "today_dday": 1,
  "nearest_event": { "title": "프로젝트 마감", "d_day": 3, "d_day_label": "D-3" }
}
```

### 3.4 터미널 대시보드 (`app/dashboard.py`)

Rich 라이브러리를 사용한 터미널 대시보드입니다:

- **KPI 패널**: 전체 이벤트 수 | 다가오는 일정 | 오늘 D-Day
- **이벤트 테이블**: 번호, 제목, 카테고리, 목표일, D-Day (색상), 메모

**D-Day 색상 규칙:**

| 조건 | 색상 | 의미 |
|------|------|------|
| `d_day == 0` | 🟣 `bold magenta` | D-Day 당일 |
| `1 ≤ d_day ≤ 3` | 🔴 `bold red` | 임박 (1~3일) |
| `4 ≤ d_day ≤ 7` | 🟡 `bold yellow` | 곧 다가옴 (4~7일) |
| `d_day > 7` | 🟢 `green` | 여유 (8일 이상) |
| `d_day < 0` | ⚫ `dim` | 이미 지남 |

### 3.5 Streamlit 웹 앱 (`streamlit_app.py`)

#### 페이지 구성

| 영역 | 내용 |
|------|------|
| **사이드바** | 새 이벤트 등록 폼 (제목, 날짜, 카테고리, 메모) |
| **KPI 카드 (4개)** | 전체 이벤트 / 다가오는 일정 / 지난 일정 / 가장 가까운 D-Day |
| **탭 1 - 이벤트 목록** | 카드 형태로 이벤트 표시 + 삭제 버튼 |
| **탭 2 - 시각화** | 도넛 차트, 바 차트, 타임라인 |

#### 커스텀 스타일 & 차트 테마

- **배경**: 그라데이션 (`#0f0c29 → #302b63 → #24243e`)
- **KPI 카드**: 글래스모피즘, `backdrop-filter: blur(10px)`, 호버 시 리프트 효과
- **이벤트 카드**: 상태별 좌측 보더 색상 (기본: `#00d4ff`, 오늘: `#ff6ec7`, 과거: `#888`)
- **차트 테마**: `plotly_dark` 템플릿 + 투명 배경

#### Plotly 차트 구성

| 차트 | 종류 | 설명 |
|------|------|------|
| 카테고리 분포 | 도넛 차트 (`go.Pie`) | 이벤트 카테고리별 비율 |
| 남은 일수 | 바 차트 (`go.Bar`) | 미래 이벤트의 D-Day 비교, 임박 이벤트 강조 |
| 타임라인 | 스캐터 (`go.Scatter`) | 전체 이벤트 시간 축 배치 + "오늘" 수직 점선 |

---

## 4. 📸 실행 화면 캡쳐

### 4.1 터미널 대시보드 (Rich)

```
┌───────────────────── 📊 요약 ─────────────────────┐
│ 전체: 8개  |  다가오는 일정: 7개  |  오늘 D-Day: 1개 │
└───────────────────────────────────────────────────┘
┌──────────────── 📅 D-Day Dashboard (2026-02-24) ────────────────┐
│ #  │ 제목                │ 카테고리 │ 목표일     │ D-Day        │ 메모              │
├────┼────────────────────┼─────────┼───────────┼──────────────┼──────────────────┤
│ 1  │ 오늘 D-Day!         │ 업무    │ 2026-02-24│ 🎉 D-Day!    │ 오늘이 바로 그날! │
│ 2  │ 프로젝트 마감        │ 업무    │ 2026-02-27│ D-3          │ 최종 보고서 제출  │
│ 3  │ 엄마 생신           │ 생일    │ 2026-03-01│ D-5          │ 케이크 주문 필요  │
│ 4  │ GitHub Copilot 시험 │ 시험    │ 2026-03-10│ D-14         │ 온라인 시험, 80분 │
│ 5  │ 제주도 여행          │ 여행    │ 2026-03-26│ D-30         │ 2박 3일 가족여행  │
│ 6  │ 결혼기념일           │ 기념일   │ 2026-04-10│ D-45         │ 레스토랑 예약    │
│ 7  │ 새해 첫날           │ 기타    │ 2027-01-01│ D-311        │ -                │
│ 8  │ 지난 이벤트 (테스트) │ 기타    │ 2026-02-17│ D+7 (지남)    │ 이미 지난 이벤트  │
└────┴────────────────────┴─────────┴───────────┴──────────────┴──────────────────┘
```
![alt text](<img/[화면 캡처]터미널 대시보드 실행.png>)

### 4.2 FastAPI Swagger UI

```
http://localhost:8000/docs
```

```
┌─────────────────────────────────────────────────────────┐
│  D-Day Counter API  v1.0.0                              │
│                                                         │
│  Health                                                 │
│    GET  /            서버 상태 확인                       │
│                                                         │
│  Events                                                 │
│    GET  /events      전체 이벤트 조회 (D-Day 계산 포함)    │
│    POST /events      새 이벤트 등록                       │
│    GET  /events/{id} 단일 이벤트 조회                     │
│    PUT  /events/{id} 이벤트 수정                          │
│    DEL  /events/{id} 이벤트 삭제                          │
│                                                         │
│  Dashboard                                              │
│    GET  /summary     대시보드 KPI 요약                    │
└─────────────────────────────────────────────────────────┘
```
![alt text](<img/[화면 캡처]Swagger UI.png>)

### 4.3 Streamlit 웹 대시보드

```
┌─ 사이드바 ──────────┐  ┌─ 메인 영역 ──────────────────────────────────┐
│                     │  │                                              │
│ ➕ 새 이벤트 등록    │  │  📅 D-Day Counter Dashboard                  │
│                     │  │  오늘: 2026-02-24                            │
│  제목: [입력]       │  │                                              │
│  목표 날짜: [달력]   │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────────┐   │
│  카테고리: [선택]    │  │  │  8   │ │  7   │ │  1   │ │ 🎉 D-Day!│   │
│  메모: [입력]       │  │  │전체  │ │다가옴│ │지남  │ │가장 가까운│   │
│                     │  │  └──────┘ └──────┘ └──────┘ └──────────┘   │
│  [등록]             │  │                                              │
│                     │  │  📋 이벤트 목록  |  📊 시각화               │
│─────────────────── │  │  ┌──────────────────────────────────────┐   │
│ 📅 D-Day Counter   │  │  │ 오늘 D-Day!  [업무]                  │   │
│    v1.0             │  │  │ 📆 2026-02-24 | 🎉 D-Day!      [🗑️]│   │
│                     │  │  ├──────────────────────────────────────┤   │
│                     │  │  │ 프로젝트 마감  [업무]                 │   │
│                     │  │  │ 📆 2026-02-27 | D-3             [🗑️]│   │
│                     │  │  ├──────────────────────────────────────┤   │
│                     │  │  │ 엄마 생신  [생일]                    │   │
│                     │  │  │ 📆 2026-03-01 | D-5             [🗑️]│   │
│                     │  │  └──────────────────────────────────────┘   │
└─────────────────────┘  └────────────────────────────────────────────┘
```

![alt text](<img/[화면 캡처]Streamlit 웹 앱 실행.png>)

### 4.4 Streamlit 시각화 탭

```
┌─── 카테고리별 분포 (도넛) ───┐  ┌─── 남은 일수 (바 차트) ──────────┐
│                              │  │                                  │
│        ┌───┐                 │  │  ▓▓                              │
│    ┌──┤시험├──┐              │  │  ▓▓  프로젝트 마감  D-3          │
│   ┌┤   └───┘  ├┐            │  │  ▓▓▓▓                            │
│  ┌┤│  업무     ││            │  │  ▓▓▓▓  엄마 생신  D-5            │
│  │└┤  여행     ├┘            │  │  ▓▓▓▓▓▓▓▓▓▓                     │
│  │ └┤  생일   ├              │  │  ▓▓▓▓▓▓▓▓▓▓  Copilot 시험 D-14  │
│  │  └┤ 기념일├               │  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓           │
│  │   └┤기타 ├               │  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  여행 D-30│
│  └────┴─────┘               │  │                                  │
└──────────────────────────────┘  └──────────────────────────────────┘

┌─── 📅 이벤트 타임라인 ──────────────────────────────────────────────┐
│                        오늘                                          │
│                         │                                            │
│  지난 이벤트 ●          │  ● 마감  ● 생신  ● 시험  ● 여행  ● 기념일 │
│  D+7(지남)              │  D-3     D-5     D-14     D-30    D-45     │
│ ─────────────── 2/17 ──┼── 2/27 ── 3/1 ── 3/10 ── 3/26 ── 4/10 ──→│
│                         │                                            │
└──────────────────────────────────────────────────────────────────────┘
```
![alt text](<img/[화면 캡처]Streamlit 시각화 탭.png>)

### 4.5 테스트 실행 결과

```
$ python -m pytest tests/ -v

========================== test session starts ==========================
platform win32 -- Python 3.14.3, pytest-9.0.2
collected 41 items

tests/test_step1_core.py::TestCalculateDday::test_future_date       PASSED [  2%]
tests/test_step1_core.py::TestCalculateDday::test_past_date         PASSED [  4%]
tests/test_step1_core.py::TestCalculateDday::test_today             PASSED [  7%]
tests/test_step1_core.py::TestCalculateDday::test_default_base_date PASSED [  9%]
tests/test_step1_core.py::TestFormatDdayLabel::test_future_label    PASSED [ 12%]
tests/test_step1_core.py::TestFormatDdayLabel::test_today_label     PASSED [ 14%]
tests/test_step1_core.py::TestFormatDdayLabel::test_past_label      PASSED [ 17%]
tests/test_step1_core.py::TestFormatDdayLabel::test_one_day_left    PASSED [ 19%]
tests/test_step1_core.py::TestFormatDdayLabel::test_one_day_past    PASSED [ 21%]
tests/test_step1_core.py::TestEventToResponse::test_response_fields PASSED [ 24%]
tests/test_step1_core.py::TestEventToResponse::test_past_event_resp PASSED [ 26%]
tests/test_step1_core.py::TestSortEvents::test_sort_order           PASSED [ 29%]
tests/test_step1_core.py::TestSortEvents::test_empty_list           PASSED [ 31%]
tests/test_step2_models.py::TestDdayEvent::test_create_with_defaults PASSED [ 34%]
tests/test_step2_models.py::TestDdayEvent::test_all_fields          PASSED [ 36%]
tests/test_step2_models.py::TestDdayEvent::test_title_min_length    PASSED [ 39%]
tests/test_step2_models.py::TestDdayEvent::test_title_max_length    PASSED [ 41%]
tests/test_step2_models.py::TestDdayEventCreate::test_minimal       PASSED [ 43%]
tests/test_step2_models.py::TestDdayEventCreate::test_with_category PASSED [ 46%]
tests/test_step2_models.py::TestEventCategory::test_all_categories  PASSED [ 48%]
tests/test_step3_storage.py::TestStorage::test_load_empty           PASSED [ 51%]
tests/test_step3_storage.py::TestStorage::test_add_and_load         PASSED [ 53%]
tests/test_step3_storage.py::TestStorage::test_add_multiple         PASSED [ 56%]
tests/test_step3_storage.py::TestStorage::test_get_event            PASSED [ 58%]
tests/test_step3_storage.py::TestStorage::test_get_nonexistent      PASSED [ 60%]
tests/test_step3_storage.py::TestStorage::test_delete_event         PASSED [ 63%]
tests/test_step3_storage.py::TestStorage::test_delete_nonexistent   PASSED [ 65%]
tests/test_step3_storage.py::TestStorage::test_update_event         PASSED [ 68%]
tests/test_step3_storage.py::TestStorage::test_update_nonexistent   PASSED [ 70%]
tests/test_step3_storage.py::TestStorage::test_json_file_format     PASSED [ 73%]
tests/test_step4_api.py::TestHealthEndpoint::test_health            PASSED [ 75%]
tests/test_step4_api.py::TestEventsEndpoints::test_create_event     PASSED [ 78%]
tests/test_step4_api.py::TestEventsEndpoints::test_list_events      PASSED [ 80%]
tests/test_step4_api.py::TestEventsEndpoints::test_category_filter  PASSED [ 82%]
tests/test_step4_api.py::TestEventsEndpoints::test_get_single       PASSED [ 85%]
tests/test_step4_api.py::TestEventsEndpoints::test_get_nonexistent  PASSED [ 87%]
tests/test_step4_api.py::TestEventsEndpoints::test_update_event     PASSED [ 90%]
tests/test_step4_api.py::TestEventsEndpoints::test_delete_event     PASSED [ 92%]
tests/test_step4_api.py::TestEventsEndpoints::test_delete_nonexist  PASSED [ 95%]
tests/test_step4_api.py::TestSummaryEndpoint::test_summary_empty    PASSED [ 97%]
tests/test_step4_api.py::TestSummaryEndpoint::test_summary_events   PASSED [100%]

======================= 41 passed in 1.19s ========================
```

> **결과: 4단계 총 41개 테스트 전부 PASSED ✅**

---

## 5. 💡 추가 기능 구현 목록

현재 D-Day Counter 앱에 추가로 구현할 수 있는 20개 기능 목록입니다.

| # | 기능 이름 | 상세 설명 |
|---|----------|----------|
| 1 | **리마인더 알림기 (Simple Reminder)** | D-Day에 대하여 매일 일정 시간에 데스크톱 알림(토스트)을 띄워주는 초간단 리마인더. `plyer` 라이브러리로 OS 네이티브 알림을 전송하고, `schedule` 라이브러리로 매일 지정 시간(예: 오전 9시)에 임박한 D-Day 이벤트 목록을 토스트 메시지로 표시. 백그라운드 프로세스로 실행되며, 알림 시간대/반복 주기를 설정 파일로 커스터마이징 가능. |
| 2 | **반복 이벤트 (Recurring Events)** | 매년 반복되는 이벤트(생일, 기념일 등)를 자동으로 다음 해로 갱신하는 기능. 이벤트 모델에 `recurrence` 필드(yearly/monthly/weekly/none)를 추가하여, D-Day가 지나면 자동으로 다음 주기의 날짜로 target_date를 갱신. |
| 3 | **카테고리별 필터 UI (Category Filter)** | Streamlit 앱에서 카테고리 버튼/셀렉트박스로 이벤트를 필터링하는 기능. "전체/시험/여행/생일/업무" 버튼을 클릭하면 해당 카테고리의 이벤트만 목록과 차트에 표시. |
| 4 | **이벤트 수정 UI (Edit Event)** | 현재 삭제만 가능한 Streamlit 앱에 인라인 수정 기능을 추가. 각 이벤트 카드에 "✏️ 수정" 버튼을 추가하여, 클릭 시 모달/expander로 제목·날짜·카테고리·메모를 수정할 수 있는 폼 표시. |
| 5 | **다크모드 / 라이트모드 토글 (Theme Toggle)** | Streamlit 앱에서 사용자가 다크/라이트 테마를 전환할 수 있는 토글 버튼. CSS 변수와 `st.session_state`를 활용하여 배경색, 글자색, 카드 스타일을 동적으로 전환. |
| 6 | **날짜 범위 필터 (Date Range Filter)** | "1주일 이내 / 1개월 이내 / 3개월 이내 / 전체" 등 날짜 범위로 이벤트를 필터링. 직접 시작일~종료일을 선택하는 날짜 피커도 제공하여 특정 기간의 이벤트만 조회. |
| 7 | **CSV/Excel 내보내기 (Export)** | 이벤트 목록을 CSV 또는 Excel 파일로 다운로드하는 기능. `pandas`로 DataFrame 변환 후 `st.download_button`으로 제공. D-Day 계산 결과까지 포함하여 내보내기. |
| 8 | **CSV/JSON 가져오기 (Import)** | 외부 CSV/JSON 파일을 업로드하여 이벤트를 일괄 등록하는 기능. `st.file_uploader`로 파일을 업로드, 형식 검증 후 기존 데이터에 병합 또는 덮어쓰기 선택 가능. |
| 9 | **검색 기능 (Search)** | 제목, 메모, 카테고리 등 키워드로 이벤트를 검색하는 기능. Streamlit 헤더에 검색바를 배치하여 실시간 필터링. FastAPI에도 `GET /events/search?q=키워드` 엔드포인트 추가. |
| 10 | **이벤트 중요도/우선순위 (Priority)** | 이벤트에 우선순위(높음/보통/낮음)를 설정하는 기능. 높은 우선순위 이벤트는 보더 색 강조, 상단 고정, 리마인더에서 우선 알림. 모델에 `priority: HIGH/MEDIUM/LOW` 필드 추가. |
| 11 | **다중 사용자 지원 (Multi-User)** | 사용자별로 독립된 이벤트 데이터를 관리하는 기능. 간단한 로그인(이름/토큰) 또는 사이드바 사용자 선택으로 각자의 D-Day 목록을 분리. JSON 파일을 사용자별로 분리하거나 SQLite DB 도입. |
| 12 | **SQLite 데이터베이스 마이그레이션 (DB Migration)** | 현재 JSON 파일 기반 저장소를 SQLite로 마이그레이션하는 기능. `SQLAlchemy` + `Alembic`을 사용하여 데이터 무결성, 동시 접근, 성능을 개선. 기존 JSON 데이터 자동 마이그레이션 스크립트 포함. |
| 13 | **D-Day 위젯 (Desktop Widget)** | 데스크톱에 항상 표시되는 소형 D-Day 위젯. `tkinter` 또는 `PyQt6`로 미니 창을 만들어 항상 최상단(Always on Top)으로 가장 가까운 3개 이벤트의 D-Day를 표시. 트레이 아이콘으로 최소화 가능. |
| 14 | **캔린더 등기화 (Calendar Sync)** | Google Calendar, Outlook 등 외부 캔린더와 동기화하는 기능. `.ics` (iCalendar) 파일로 내보내기/가져오기를 지원하여 이벤트를 다른 캔린더 앱에 추가하거나, 외부 캔린더 일정을 D-Day로 가져오기. |
| 15 | **통계 대시보드 (Statistics Dashboard)** | 월별/카테고리별 이벤트 통계를 시각화하는 전용 페이지. 월별 이벤트 수 히트맵, 완료/미래 비율 게이지, 가장 바쁜 달 분석, 카테고리별 트렌드 라인 차트 등 Plotly 기반 고급 시각화. |
| 16 | **이벤트 색상 커스터마이징 (Color Tags)** | 사용자가 이벤트별로 색상 태그를 지정하는 기능. 커러 피커로 10여 가지 색상 중 선택하면 이벤트 카드 좌측 보더/배지에 반영. 차트에서도 사용자 지정 색상으로 표시. |
| 17 | **공유 링크 생성 (Share Link)** | 특정 이벤트를 URL로 공유하는 기능. 이벤트 정보를 쿼리 파라미터로 인코딩한 공유 URL을 생성하거나, FastAPI에 공유 전용 `GET /share/{token}` 엔드포인트를 추가하여 읽기 전용 D-Day 페이지 제공. |
| 18 | **완료/아카이브 기능 (Archive)** | 지난 이벤트를 자동 또는 수동으로 아카이브하는 기능. 아카이브된 이벤트는 기본 목록에서 숨기고, "아카이브" 탭에서 별도 조회. 삭제와 달리 복원이 가능하며 지난 이벤트 이력 관리에 유용. |
| 19 | **다국어 지원 (i18n)** | 한국어/영어 등 다국어 UI를 지원하는 기능. 라벨 문자열을 JSON 로케일 파일(`locales/ko.json`, `locales/en.json`)로 분리하고, 사이드바 언어 선택기로 전체 UI 텍스트를 동적 전환. |
| 20 | **PWA / 모바일 반응형 UI (Mobile Responsive)** | Streamlit 앱을 모바일 환경에서도 쟘 보이도록 반응형 CSS를 개선하는 기능. KPI 카드를 모바일에서 2열 레이아웃으로 전환, 이벤트 카드 폰트 조정, 차트 높이 자동 조정. `@media` 쿼리로 브레이크포인트별 스타일 최적화. |

---

## 📄 라이선스

이 프로젝트는 학습 목적으로 제작되었습니다.
