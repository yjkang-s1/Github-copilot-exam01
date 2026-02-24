"""
샘플 D-Day 데이터 생성 스크립트
실행: python generate_sample_data.py
"""

from datetime import date, timedelta

from app.models import DdayEventCreate, EventCategory
from app.storage import add_event, save_events, DEFAULT_DATA_PATH

# 기존 데이터 초기화
save_events([], DEFAULT_DATA_PATH)

sample_events = [
    DdayEventCreate(
        title="GitHub Copilot 자격시험",
        target_date=date.today() + timedelta(days=14),
        category=EventCategory.EXAM,
        memo="온라인 시험, 80분",
    ),
    DdayEventCreate(
        title="제주도 여행",
        target_date=date.today() + timedelta(days=30),
        category=EventCategory.TRAVEL,
        memo="2박 3일 가족여행",
    ),
    DdayEventCreate(
        title="엄마 생신",
        target_date=date.today() + timedelta(days=5),
        category=EventCategory.BIRTHDAY,
        memo="케이크 주문 필요",
    ),
    DdayEventCreate(
        title="결혼기념일",
        target_date=date.today() + timedelta(days=45),
        category=EventCategory.ANNIVERSARY,
        memo="레스토랑 예약",
    ),
    DdayEventCreate(
        title="프로젝트 마감",
        target_date=date.today() + timedelta(days=3),
        category=EventCategory.WORK,
        memo="최종 보고서 제출",
    ),
    DdayEventCreate(
        title="새해 첫날",
        target_date=date(2027, 1, 1),
        category=EventCategory.OTHER,
        memo=None,
    ),
    DdayEventCreate(
        title="지난 이벤트 (테스트)",
        target_date=date.today() - timedelta(days=7),
        category=EventCategory.OTHER,
        memo="이미 지난 이벤트",
    ),
    DdayEventCreate(
        title="오늘 D-Day!",
        target_date=date.today(),
        category=EventCategory.WORK,
        memo="오늘이 바로 그날!",
    ),
]

print("📅 샘플 데이터 생성 중...")
for ev in sample_events:
    created = add_event(ev)
    print(f"  ✅ {created.title} ({created.target_date}) - ID: {created.id}")

print(f"\n✅ {len(sample_events)}개의 샘플 이벤트가 생성되었습니다!")
print(f"📂 저장 위치: {DEFAULT_DATA_PATH}")
