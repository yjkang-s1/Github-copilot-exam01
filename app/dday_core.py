"""
D-Day Counter - 핵심 비즈니스 로직
날짜 계산, 정렬, 레이블 생성 등 핵심 기능을 담당합니다.
"""

from __future__ import annotations

from datetime import date
from typing import List

from app.models import DdayEvent, DdayEventResponse


def calculate_dday(target_date: date, base_date: date | None = None) -> int:
    """
    D-Day를 계산합니다.
    반환값: 양수 → 남은 일수, 0 → 오늘, 음수 → 지난 일수
    """
    if base_date is None:
        base_date = date.today()
    delta = (target_date - base_date).days
    return delta


def format_dday_label(d_day: int) -> str:
    """
    D-Day 값을 사람이 읽기 쉬운 레이블로 변환합니다.
    예: -3 → "D+3 (지남)", 0 → "🎉 D-Day!", 5 → "D-5"
    """
    if d_day > 0:
        return f"D-{d_day}"
    elif d_day == 0:
        return "🎉 D-Day!"
    else:
        return f"D+{abs(d_day)} (지남)"


def event_to_response(event: DdayEvent, base_date: date | None = None) -> DdayEventResponse:
    """DdayEvent를 D-Day 계산 결과가 포함된 응답 모델로 변환합니다."""
    d_day = calculate_dday(event.target_date, base_date)
    return DdayEventResponse(
        id=event.id,
        title=event.title,
        target_date=event.target_date,
        category=event.category,
        memo=event.memo,
        created_at=event.created_at,
        d_day=d_day,
        d_day_label=format_dday_label(d_day),
        is_past=d_day < 0,
    )


def sort_events_by_proximity(
    events: List[DdayEvent],
    base_date: date | None = None,
) -> List[DdayEventResponse]:
    """
    이벤트 목록을 오늘 기준으로 가까운 순서(미래 우선, 그 다음 과거)로 정렬합니다.
    """
    responses = [event_to_response(e, base_date) for e in events]
    # 미래 이벤트(d_day >= 0)를 먼저, 남은 일수 오름차순
    # 과거 이벤트(d_day < 0)를 뒤에, 지난 일수 오름차순(절대값)
    future = sorted([r for r in responses if r.d_day >= 0], key=lambda r: r.d_day)
    past = sorted([r for r in responses if r.d_day < 0], key=lambda r: abs(r.d_day))
    return future + past
