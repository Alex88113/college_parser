import pytest
import httpx
import respx

from src.college_parser.services.auth_services import AuthService


@pytest.mark.asyncio
async def test_authorization_success():
    """Тест успешной авторизации с respx"""

    # Данные для теста
    user_data = {"email": "test@example.com", "password": "password123"}
    headers = {"Content-Type": "application/json"}

    # Ожидаемый ответ от сервера
    expected_response = {
        "token": "eyJhbGciOiJIUzI1NiIs...",
        "user_id": 123,
        "expires_in": 3600
    }

    # Используем контекстный менеджер respx.mock (асинхронно)[citation:5][citation:9]
    async with respx.mock:
        # Мокаем POST запрос на URL твоей авторизации
        respx.post("https://msapi.top-academy.ru/api/v2/auth/login").mock(
            return_value=httpx.Response(200, json=expected_response)
        )

        # Выполняем реальный код сервиса
        async with AuthService() as auth_service:
            result = await auth_service.authorization(user_data, headers)

    # Проверки
    assert result["token"] == expected_response["token"]
    assert result["user_id"] == 123