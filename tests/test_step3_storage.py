"""
단계 3 테스트: 데이터 저장소 (storage) CRUD 검증
"""

import json
import pytest
from datetime import date
from pathlib import Path

from app.models import DdayEventCreate, EventCategory
from app.storage import (
    add_event,
    delete_event,
    get_event,
    load_events,
    save_events,
    update_event,
)
from app.models import DdayEvent


@pytest.fixture
def tmp_data_path(tmp_path) -> Path:
    """임시 JSON 파일 경로를 제공합니다."""
    return tmp_path / "test_events.json"


class TestStorage:
    """저장소 CRUD 테스트"""

    def test_load_empty(self, tmp_data_path):
        """파일이 없으면 빈 리스트 반환"""
        events = load_events(tmp_data_path)
        assert events == []

    def test_add_and_load(self, tmp_data_path):
        """이벤트 추가 후 로드"""
        payload = DdayEventCreate(title="시험", target_date=date(2026, 6, 15), category=EventCategory.EXAM)
        new_event = add_event(payload, tmp_data_path)
        assert new_event.title == "시험"

        loaded = load_events(tmp_data_path)
        assert len(loaded) == 1
        assert loaded[0].title == "시험"

    def test_add_multiple(self, tmp_data_path):
        """여러 이벤트 추가"""
        for i in range(3):
            add_event(DdayEventCreate(title=f"이벤트{i}", target_date=date(2026, 3, i + 1)), tmp_data_path)
        loaded = load_events(tmp_data_path)
        assert len(loaded) == 3

    def test_get_event(self, tmp_data_path):
        """단일 이벤트 조회"""
        created = add_event(DdayEventCreate(title="여행", target_date=date(2026, 7, 1)), tmp_data_path)
        found = get_event(created.id, tmp_data_path)
        assert found is not None
        assert found.title == "여행"

    def test_get_nonexistent(self, tmp_data_path):
        """존재하지 않는 ID 조회"""
        assert get_event("없는id", tmp_data_path) is None

    def test_delete_event(self, tmp_data_path):
        """이벤트 삭제"""
        created = add_event(DdayEventCreate(title="삭제 테스트", target_date=date(2026, 8, 1)), tmp_data_path)
        assert delete_event(created.id, tmp_data_path) is True
        assert load_events(tmp_data_path) == []

    def test_delete_nonexistent(self, tmp_data_path):
        """없는 이벤트 삭제 시 False"""
        assert delete_event("없는id", tmp_data_path) is False

    def test_update_event(self, tmp_data_path):
        """이벤트 수정"""
        created = add_event(
            DdayEventCreate(title="원래 제목", target_date=date(2026, 9, 1)),
            tmp_data_path,
        )
        updated = update_event(
            created.id,
            DdayEventCreate(title="수정된 제목", target_date=date(2026, 9, 15)),
            tmp_data_path,
        )
        assert updated is not None
        assert updated.title == "수정된 제목"
        assert updated.target_date == date(2026, 9, 15)
        assert updated.id == created.id  # ID 유지

    def test_update_nonexistent(self, tmp_data_path):
        """없는 이벤트 수정 시 None"""
        result = update_event("없는id", DdayEventCreate(title="X", target_date=date(2026, 1, 1)), tmp_data_path)
        assert result is None

    def test_json_file_format(self, tmp_data_path):
        """저장된 JSON 파일 형식 검증"""
        add_event(DdayEventCreate(title="포맷 테스트", target_date=date(2026, 5, 5)), tmp_data_path)
        with open(tmp_data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        assert isinstance(raw, list)
        assert len(raw) == 1
        assert "title" in raw[0]
        assert "target_date" in raw[0]
