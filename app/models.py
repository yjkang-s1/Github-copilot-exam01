"""
D-Day Counter - 데이터 모델 정의
Pydantic 모델을 사용하여 D-Day 이벤트의 스키마를 정의합니다.
"""

from __future__ import annotations

import uuid
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventCategory(str, Enum):
    """이벤트 카테고리 열거형"""
    EXAM = "시험"
    TRAVEL = "여행"
    BIRTHDAY = "생일"
    ANNIVERSARY = "기념일"
    WORK = "업무"
    OTHER = "기타"


class DdayEvent(BaseModel):
    """D-Day 이벤트 모델"""
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    title: str = Field(..., min_length=1, max_length=100, description="이벤트 제목")
    target_date: date = Field(..., description="목표 날짜 (YYYY-MM-DD)")
    category: EventCategory = Field(default=EventCategory.OTHER, description="카테고리")
    memo: Optional[str] = Field(default=None, max_length=200, description="메모")
    created_at: datetime = Field(default_factory=datetime.now, description="생성 시각")

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class DdayEventCreate(BaseModel):
    """이벤트 생성 요청 모델 (id/created_at 자동 생성)"""
    title: str = Field(..., min_length=1, max_length=100)
    target_date: date
    category: EventCategory = EventCategory.OTHER
    memo: Optional[str] = None


class DdayEventResponse(BaseModel):
    """이벤트 응답 모델 (D-Day 계산 결과 포함)"""
    id: str
    title: str
    target_date: date
    category: EventCategory
    memo: Optional[str]
    created_at: datetime
    d_day: int  # 음수: 지남, 0: 오늘, 양수: 남음
    d_day_label: str  # "D-3", "D-Day", "D+5" 등
    is_past: bool
