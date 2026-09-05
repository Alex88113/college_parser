import os

import httpx
import pytest
import respx
from dotenv import load_dotenv
from httpx import Response

load_dotenv()


class TestAuthService:
    """Тест успешной авторизации"""

    @pytest.mark.asyncio
    async def test_login_success(self):
        auth_url = os.getenv("AUTH_URL")

        test_username = "test_username"
        test_password = "test_password"
        test_app_key = "test_key_123"

        with respx.mock:
            mock_request = respx.post(
                auth_url,
                json={
                    "username": test_username,
                    "password": test_password,
                    "application_key": test_app_key,
                },
            ).mock(
                return_value=Response(
                    status_code=200,
                    json={
                        "refresh_token": "test_refresh",
                        "access_token": "test-access-token",
                    },
                )
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    os.getenv("AUTH_URL"),
                    json={
                        "username": test_username,
                        "password": test_password,
                        "application_key": test_app_key,
                    },
                )

            assert response.status_code == 200
            assert response.json()["refresh_token"] == "test_refresh"
            assert response.json()["access_token"] == "test-access-token"
            assert response.json() is not None
            assert isinstance(response.json(), dict)
            assert mock_request.called
