import os

import pytest
import respx
import httpx
from httpx import Response
from dotenv import load_dotenv

from src.college_parser.services.auth_services import AuthService, get_post_response
from src.college_parser.configs.user_config import config_user
from src.college_parser.headers.post_headers import get_post_headers

load_dotenv()

class TestAuthService:
    """Тест успешной авторизации"""

    @pytest.mark.asyncio
    async def test_login_success(self):
        auth_url = os.getenv('AUTH_URL')

        test_username = 'test_username'
        test_password = 'test_password'
        test_app_key = 'test_key_123'

        with respx.mock:
            mock_request = respx.post(
                auth_url,
                json={
                    "username": test_username,
                    'password': test_password,
                    'application_key': test_app_key
                }
            ).mock(
                return_value=Response(
                    status_code=200,
                    json={
                        "refresh_token": 'test_refresh',
                        'access_token': 'test-access-token'}
                )
            )
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    os.getenv('AUTH_URL'),
                    json={
                        "username": test_username,
                        "password": test_password,
                        "application_key": test_app_key}
                )

            assert response.status_code == 200
            assert response.json()['refresh_token'] == 'test_refresh'
            assert response.json()['access_token'] == 'test-access-token'
            assert response.json() is not None
            assert isinstance(response.json(), dict)

    @pytest.mark.asyncio
    async def test_auth_service(self):
        """Тестирование реального API"""
        headers_post: dict[str, str] = get_post_headers()

        with respx.mock:
            mock_request = respx.post(
                json={
                    'username': config_user.JOURNAL_NAME,
                    'password': config_user.JOURNAL_PASSWORD,
                    'application_key': config_user.APP_KEY
                }
            ).mock(
                return_value=Response(
                    status_code=200,
                    json={
                        "refresh_token": 'test_refreshjnjrnjnrjg',
                        'access_token': 'test-access-tokenrgrgnn'
                    }
                )
            )
            async with AuthService() as client:
                response = await client.authorization(
                    {
                        'username': config_user.JOURNAL_NAME,
                        'password': config_user.JOURNAL_PASSWORD,
                        'application_key': config_user.APP_KEY
                    },
                    headers_post
                )

            assert response['refresh_token'] is not None
            assert response['access_token'] is not None

            assert len(response['access_token']) > 20
            assert len(response['refresh_token']) > 20
            assert len(response['access_token']) != ""
            assert len(response['refresh_token']) != ""

            assert isinstance(response['access_token'], str)
            assert isinstance(response['refresh_token'], str)