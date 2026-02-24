"""
단계 4 테스트: FastAPI 엔드포인트 검증
"""

import pytest
from datetime import date
from fastapi.testclient import TestClient
from pathlib import Path

from app.api import app
from app import storage as storage_module

client = TestClient(app)


@pytest.fixture(autouse=True)
def use_temp_storage(tmp_path, monkeypatch):
    """모든 테스트에서 임시 저장소 사용"""
    temp_path = tmp_path / "test_events.json"
    monkeypatch.setattr(storage_module, "DEFAULT_DATA_PATH", temp_path)


class TestHealthEndpoint:
    """헬스 체크 테스트"""

    def test_health(self):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"


class TestEventsEndpoints:
    """이벤트 CRUD 엔드포인트 테스트"""

    def _create_event(self, title="시험", target_date="2026-06-15", category="시험"):
        return client.post("/events", json={
            "title": title,
            "target_date": target_date,
            "category": category,
        })

    def test_create_event(self):
        resp = self._create_event()
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "시험"
        assert "d_day" in data
        assert "d_day_label" in data

    def test_list_events(self):
        self._create_event("이벤트A", "2026-04-01")
        self._create_event("이벤트B", "2026-05-01")
        resp = client.get("/events")
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) == 2

    def test_list_with_category_filter(self):
        self._create_event("시험1", "2026-06-01", "시험")
        self._create_event("여행1", "2026-07-01", "여행")
        resp = client.get("/events", params={"category": "시험"})
        events = resp.json()
        assert len(events) == 1
        assert events[0]["title"] == "시험1"

    def test_get_single_event(self):
        created = self._create_event().json()
        resp = client.get(f"/events/{created['id']}")
        assert resp.status_code == 200
        assert resp.json()["title"] == "시험"

    def test_get_nonexistent_event(self):
        resp = client.get("/events/없는id")
        assert resp.status_code == 404

    def test_update_event(self):
        created = self._create_event().json()
        resp = client.put(f"/events/{created['id']}", json={
            "title": "수정된 시험",
            "target_date": "2026-07-01",
            "category": "시험",
        })
        assert resp.status_code == 200
        assert resp.json()["title"] == "수정된 시험"

    def test_delete_event(self):
        created = self._create_event().json()
        resp = client.delete(f"/events/{created['id']}")
        assert resp.status_code == 200
        # 삭제 확인
        resp2 = client.get(f"/events/{created['id']}")
        assert resp2.status_code == 404

    def test_delete_nonexistent(self):
        resp = client.delete("/events/없는id")
        assert resp.status_code == 404


class TestSummaryEndpoint:
    """대시보드 요약 엔드포인트 테스트"""

    def test_summary_empty(self):
        resp = client.get("/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0

    def test_summary_with_events(self):
        client.post("/events", json={"title": "미래", "target_date": "2026-12-25", "category": "기타"})
        client.post("/events", json={"title": "과거", "target_date": "2025-01-01", "category": "기타"})
        resp = client.get("/summary")
        data = resp.json()
        assert data["total"] == 2
        assert data["upcoming"] >= 1
