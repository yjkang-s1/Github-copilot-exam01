"""
단계 1 테스트: D-Day 핵심 로직 (dday_core) 검증
"""

import pytest
from datetime import date

from app.dday_core import calculate_dday, format_dday_label, event_to_response, sort_events_by_proximity
from app.models import DdayEvent, EventCategory


# ───────── calculate_dday 테스트 ─────────


class TestCalculateDday:
    """D-Day 계산 함수 테스트"""

    def test_future_date(self):
        """미래 날짜 → 양수 반환"""
        result = calculate_dday(date(2026, 3, 10), base_date=date(2026, 3, 1))
        assert result == 9

    def test_past_date(self):
        """과거 날짜 → 음수 반환"""
        result = calculate_dday(date(2026, 2, 20), base_date=date(2026, 2, 24))
        assert result == -4

    def test_today(self):
        """오늘 날짜 → 0 반환"""
        today = date.today()
        result = calculate_dday(today, base_date=today)
        assert result == 0

    def test_default_base_date(self):
        """base_date 미지정 시 오늘 기준"""
        result = calculate_dday(date.today())
        assert result == 0


# ───────── format_dday_label 테스트 ─────────


class TestFormatDdayLabel:
    """D-Day 레이블 포맷 테스트"""

    def test_future_label(self):
        assert format_dday_label(5) == "D-5"

    def test_today_label(self):
        assert format_dday_label(0) == "🎉 D-Day!"

    def test_past_label(self):
        assert format_dday_label(-3) == "D+3 (지남)"

    def test_one_day_left(self):
        assert format_dday_label(1) == "D-1"

    def test_one_day_past(self):
        assert format_dday_label(-1) == "D+1 (지남)"


# ───────── event_to_response 테스트 ─────────


class TestEventToResponse:
    """이벤트 → 응답 변환 테스트"""

    def _make_event(self, target_date: date) -> DdayEvent:
        return DdayEvent(
            id="test001",
            title="테스트 이벤트",
            target_date=target_date,
            category=EventCategory.EXAM,
        )

    def test_response_fields(self):
        event = self._make_event(date(2026, 3, 1))
        resp = event_to_response(event, base_date=date(2026, 2, 24))
        assert resp.id == "test001"
        assert resp.title == "테스트 이벤트"
        assert resp.d_day == 5
        assert resp.d_day_label == "D-5"
        assert resp.is_past is False

    def test_past_event_response(self):
        event = self._make_event(date(2026, 2, 20))
        resp = event_to_response(event, base_date=date(2026, 2, 24))
        assert resp.d_day == -4
        assert resp.is_past is True


# ───────── sort_events_by_proximity 테스트 ─────────


class TestSortEvents:
    """이벤트 정렬 테스트"""

    def test_sort_order(self):
        """미래 이벤트(가까운 순) → 과거 이벤트(최근 순) 정렬"""
        base = date(2026, 3, 1)
        events = [
            DdayEvent(id="a", title="먼 미래", target_date=date(2026, 4, 1), category=EventCategory.TRAVEL),
            DdayEvent(id="b", title="가까운 미래", target_date=date(2026, 3, 3), category=EventCategory.EXAM),
            DdayEvent(id="c", title="과거", target_date=date(2026, 2, 20), category=EventCategory.BIRTHDAY),
            DdayEvent(id="d", title="오늘", target_date=date(2026, 3, 1), category=EventCategory.OTHER),
        ]
        result = sort_events_by_proximity(events, base_date=base)
        titles = [r.title for r in result]
        assert titles == ["오늘", "가까운 미래", "먼 미래", "과거"]

    def test_empty_list(self):
        assert sort_events_by_proximity([]) == []
