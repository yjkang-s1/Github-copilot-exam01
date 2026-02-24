"""
D-Day Counter - FastAPI 백엔드
RESTful API 엔드포인트를 제공합니다.
"""

from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.dday_core import event_to_response, sort_events_by_proximity
from app.models import DdayEventCreate, DdayEventResponse, EventCategory
from app.storage import add_event, delete_event, get_event, load_events, update_event

app = FastAPI(
    title="D-Day Counter API",
    description="중요한 날짜를 등록하고 D-Day를 관리하는 REST API",
    version="1.0.0",
)

# CORS 허용 (Streamlit 등 프론트엔드 연동)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ───────── 엔드포인트 ─────────


@app.get("/", tags=["Health"])
def health_check():
    """서버 상태 확인"""
    return {"status": "ok", "message": "D-Day Counter API is running 🚀"}


@app.get("/events", response_model=List[DdayEventResponse], tags=["Events"])
def list_events(
    category: Optional[EventCategory] = Query(None, description="카테고리 필터"),
    sort: bool = Query(True, description="가까운 순 정렬 여부"),
):
    """
    전체 이벤트 목록 조회 (D-Day 계산 포함)
    - category: 선택적 카테고리 필터
    - sort: True면 가까운 순 정렬
    """
    events = load_events()
    if category:
        events = [e for e in events if e.category == category]
    if sort:
        return sort_events_by_proximity(events)
    return [event_to_response(e) for e in events]


@app.get("/events/{event_id}", response_model=DdayEventResponse, tags=["Events"])
def get_single_event(event_id: str):
    """단일 이벤트 조회"""
    event = get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return event_to_response(event)


@app.post("/events", response_model=DdayEventResponse, status_code=201, tags=["Events"])
def create_event(payload: DdayEventCreate):
    """새 이벤트 등록"""
    new_event = add_event(payload)
    return event_to_response(new_event)


@app.put("/events/{event_id}", response_model=DdayEventResponse, tags=["Events"])
def modify_event(event_id: str, payload: DdayEventCreate):
    """이벤트 수정"""
    updated = update_event(event_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return event_to_response(updated)


@app.delete("/events/{event_id}", tags=["Events"])
def remove_event(event_id: str):
    """이벤트 삭제"""
    success = delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="이벤트를 찾을 수 없습니다.")
    return {"detail": "삭제되었습니다.", "id": event_id}


@app.get("/summary", tags=["Dashboard"])
def summary():
    """대시보드 요약 KPI"""
    events = load_events()
    responses = sort_events_by_proximity(events)
    total = len(responses)
    upcoming = sum(1 for r in responses if r.d_day >= 0)
    past = total - upcoming
    today = sum(1 for r in responses if r.d_day == 0)
    nearest = responses[0] if responses else None
    return {
        "total": total,
        "upcoming": upcoming,
        "past": past,
        "today_dday": today,
        "nearest_event": nearest,
    }
