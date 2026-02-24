"""
D-Day Counter - 데이터 저장소 (JSON 파일 기반)
이벤트의 CRUD 및 영속성을 관리합니다.
"""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

from app.models import DdayEvent, DdayEventCreate

# 기본 데이터 파일 경로
DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "events.json"


def _ensure_data_dir(path: Path) -> None:
    """데이터 디렉토리가 없으면 생성합니다."""
    path.parent.mkdir(parents=True, exist_ok=True)


def _serialize_event(event: DdayEvent) -> dict:
    """DdayEvent를 JSON 직렬화 가능한 dict로 변환합니다."""
    d = event.model_dump()
    d["target_date"] = event.target_date.isoformat()
    d["created_at"] = event.created_at.isoformat()
    return d


def _deserialize_event(data: dict) -> DdayEvent:
    """dict를 DdayEvent로 역직렬화합니다."""
    data["target_date"] = date.fromisoformat(data["target_date"])
    data["created_at"] = datetime.fromisoformat(data["created_at"])
    return DdayEvent(**data)


def load_events(path: Path | None = None) -> List[DdayEvent]:
    """JSON 파일에서 이벤트 목록을 로드합니다."""
    path = path or DEFAULT_DATA_PATH
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [_deserialize_event(item) for item in raw]


def save_events(events: List[DdayEvent], path: Path | None = None) -> None:
    """이벤트 목록을 JSON 파일로 저장합니다."""
    path = path or DEFAULT_DATA_PATH
    _ensure_data_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([_serialize_event(e) for e in events], f, ensure_ascii=False, indent=2)


def add_event(event_create: DdayEventCreate, path: Path | None = None) -> DdayEvent:
    """새 이벤트를 추가하고 저장합니다."""
    events = load_events(path)
    new_event = DdayEvent(
        title=event_create.title,
        target_date=event_create.target_date,
        category=event_create.category,
        memo=event_create.memo,
    )
    events.append(new_event)
    save_events(events, path)
    return new_event


def delete_event(event_id: str, path: Path | None = None) -> bool:
    """이벤트 ID로 삭제합니다. 성공 시 True 반환."""
    events = load_events(path)
    filtered = [e for e in events if e.id != event_id]
    if len(filtered) == len(events):
        return False
    save_events(filtered, path)
    return True


def get_event(event_id: str, path: Path | None = None) -> Optional[DdayEvent]:
    """이벤트 ID로 단일 이벤트를 조회합니다."""
    events = load_events(path)
    for e in events:
        if e.id == event_id:
            return e
    return None


def update_event(event_id: str, event_create: DdayEventCreate, path: Path | None = None) -> Optional[DdayEvent]:
    """이벤트를 수정합니다."""
    events = load_events(path)
    for i, e in enumerate(events):
        if e.id == event_id:
            updated = DdayEvent(
                id=e.id,
                title=event_create.title,
                target_date=event_create.target_date,
                category=event_create.category,
                memo=event_create.memo,
                created_at=e.created_at,
            )
            events[i] = updated
            save_events(events, path)
            return updated
    return None
