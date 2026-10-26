import pytest
from httpx import ASGITransport, AsyncClient

from src.college_parser.main import app
from src.college_parser.routers import today_router


@pytest.mark.asyncio
async def test_today_schedule_router(monkeypatch):
    """Тест роутера /schedule/today с замоканным сервисом."""

    async def fake_get_schedule_today() -> str:
        return "Расписание на сегодня\nПара: Тестовая"

    monkeypatch.setattr(
        today_router,
        "get_schedule_today",
        fake_get_schedule_today,
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/schedule/today")

    assert response.status_code == 200
    assert "Расписание на сегодня" in response.text
    assert "Тестовая" in response.text
