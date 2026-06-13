import asyncio
from typing import List, Dict

import httpx

from src.college_parser.configs.user_config import config_user, get_user_config
from src.college_parser.headers.post_headers import get_post_headers


class AuthService:
    def __init__(
            self,
            timeout: float = 30.0,
            max_connection: int = 100,
            max_keepalive_connection: int = 20
    ) -> None:
        self.timeout = timeout
        self.max_connection = max_connection
        self.max_keepalive_connection =  max_keepalive_connection
        self.limits = httpx.Limits(
            max_keepalive_connections=max_keepalive_connection,
            max_connections=self.max_connection)
        self.auth_url: str = str(config_user.AUTH_URL)
        self.get_url: str = str(config_user.BASE_URL)
        self._client = None

    async def _get_connection(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                limits=self.limits,
                headers={'Accept': 'application/json, text/plain, */*'}
            )
            return self._client
        return self._client

    # open connection
    async def __aenter__(self) -> "AuthService":
        await self._get_connection()
        return self

    # closing the connection
    async def __aexit__(self, *args) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def authorization(
            self,
            user_data: Dict[str, str],
            headers: Dict[str, str],
    ) -> Dict[str, str | int]:
        client = await self._get_connection()
        try:
            response = await client.post(self.auth_url, json=user_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.ConnectTimeout as error:
            raise httpx.ConnectTimeout(f"Не удалось подключится к серверу: {error}") from error

        except httpx.TimeoutException as error:
            raise httpx.TimeoutException(f"Таймаут на подключение истек: {error}") from error

async def get_post_response() -> dict[str, str | int]:
    user_data: Dict[str, str] = get_user_config()
    headers: Dict[str, str] = get_post_headers()
    async with AuthService() as auth_service:
        return await auth_service.authorization(user_data, headers)

