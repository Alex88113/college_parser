import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from src.college_parser.routers.today_router import router, get_today_schedule_view

client = TestClient(router)

def test_today_schedule_router() -> None:
    response = client.get('/schedule/today')
    assert response.headers['content-type'] == 'text/html; charset=utf-8'