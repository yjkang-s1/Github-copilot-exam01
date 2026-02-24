"""
단계 2 테스트: 데이터 모델 (models) 검증
"""

import pytest
from datetime import date, datetime

from app.models import DdayEvent, DdayEventCreate, DdayEventResponse, EventCategory


class TestDdayEvent:
    """DdayEvent 모델 테스트"""

    def test_create_with_defaults(self):
        event = DdayEvent(title="시험", target_date=date(2026, 6, 15))
        assert event.title == "시험"
        assert event.category == EventCategory.OTHER
        assert event.memo is None
        assert len(event.id) == 8  # uuid hex[:8]
        assert isinstance(event.created_at, datetime)

    def test_all_fields(self):
        event = DdayEvent(
            id="abc12345",
            title="여행",
            target_date=date(2026, 7, 1),
            category=EventCategory.TRAVEL,
            memo="제주도 여행",
        )
        assert event.id == "abc12345"
        assert event.category == EventCategory.TRAVEL
        assert event.memo == "제주도 여행"

    def test_title_min_length(self):
        with pytest.raises(Exception):
            DdayEvent(title="", target_date=date(2026, 1, 1))

    def test_title_max_length(self):
        with pytest.raises(Exception):
            DdayEvent(title="A" * 101, target_date=date(2026, 1, 1))


class TestDdayEventCreate:
    """DdayEventCreate 모델 테스트"""

    def test_minimal_create(self):
        payload = DdayEventCreate(title="생일", target_date=date(2026, 5, 5))
        assert payload.title == "생일"
        assert payload.category == EventCategory.OTHER

    def test_with_category(self):
        payload = DdayEventCreate(
            title="기말고사",
            target_date=date(2026, 6, 20),
            category=EventCategory.EXAM,
            memo="3층 강의실",
        )
        assert payload.category == EventCategory.EXAM


class TestEventCategory:
    """카테고리 열거형 테스트"""

    def test_all_categories(self):
        expected = {"시험", "여행", "생일", "기념일", "업무", "기타"}
        actual = {c.value for c in EventCategory}
        assert actual == expected
