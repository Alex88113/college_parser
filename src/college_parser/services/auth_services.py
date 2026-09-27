import asyncio
from typing import Annotated

import httpx

from src.college_parser.configs.user_config import config_user, get_user_config
from src.college_parser.headers.post_headers import get_post_headers
from src.college_parser.services.redis_service import RedisService
from src.college_parser.utils.logger import logger

_client: Annotated[
    httpx.AsyncClient | None, "Асинхронный клиент для отправки http запросов"
] = None
_client_lock: asyncio.Lock = asyncio.Lock()
semaphore: Annotated[asyncio.Semaphore, "Ограничитель запросов к API"] = (
    asyncio.Semaphore(3)
)


class HTTPClient:
    def __init__(self) -> None:
        self._timeout = httpx.Timeout(connect=10.0, read=30.0, write=10.0, pool=5.0)
        self._limits = httpx.Limits(
            max_connections=100, max_keepalive_connections=25, keepalive_expiry=30.0
        )
        self._transport: Annotated[
            httpx.AsyncHTTPTransport, "Добавление Retries для повторных запросов"
        ] = httpx.AsyncHTTPTransport(retries=3)

    async def __aenter__(self) -> httpx.AsyncClient:
        global _client
        async with _client_lock:
            if _client is None:
                _client = httpx.AsyncClient(
                    timeout=self._timeout,
                    limits=self._limits,
                    transport=self._transport,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/150.0.0.0 YaBrowser/26.8.0.0 Safari/537.36"
                    },
                )

            return _client

    async def __aexit__(self, *args) -> None:
        global _client
        async with _client_lock:
            if _client:
                await _client.aclose()
                _client = None


class AuthService:
    def __init__(self, redis_service: RedisService, client: httpx.AsyncClient) -> None:
        self._redis_service = redis_service
        self._client = client
        self.auth_url: str = str(config_user.AUTH_URL)
        self.get_url: str = str(config_user.BASE_URL)

    async def authorization(
        self,
        method: str,
        user_data: dict[str, str],
        headers: dict[str, str],
    ) -> dict[str, str | int]:
        try:
            async with semaphore:
                response = await self._client.request(
                    method, self.auth_url, json=user_data, headers=headers
                )
                response.raise_for_status()
                return response.json()
        except httpx.ConnectTimeout as error:
            raise httpx.ConnectTimeout(
                f"Не удалось подключится к серверу: {error}"
            ) from error
        except httpx.TimeoutException as error:
            raise httpx.TimeoutException(
                f"Таймаут на подключение истек: {error}"
            ) from error
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 401:
                logger.error("Неверный логин или пароль.")
            else:
                logger.error(f"API вернул ошибку: {error}")
            raise

    async def refresh_token(
        self,
        method: str,
        refresh_token: str,
        headers: dict[str, str],
    ) -> dict[str, str | int]:
        """Метод обновления refresh токена"""
        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        try:
            async with semaphore:
                response = await self._client.request(
                    method, self.auth_url, data=data, headers=headers
                )
                response.raise_for_status()
        except httpx.ConnectTimeout as error:
            raise httpx.ConnectTimeout(
                f"Не удалось подключится к серверу: {error}"
            ) from error
        except httpx.TimeoutException as error:
            raise httpx.TimeoutException(
                f"Таймаут на подключение истек: {error}"
            ) from error
        except httpx.HTTPStatusError as error:
            if error.response.status_code == 401:
                logger.error("Недостаточно прав доступа.")
            else:
                logger.error(f"API вернул ошибку: {error}")
            raise
        else:
            return response.json()

    async def get_valid_access_token(
        self,
        method: str,
        key: str,
        headers: dict[str, str],
    ) -> str | None:
        client = await self._redis_service.get_client()
        """ Проверяем есть ли сам токен в кэше если есть находим и проверяем протух он или нет"""
        if await client.exists(key):
            ttl_value: int = await client.ttl(key)
            if ttl_value > 0:
                return await client.get(key)
            else:
                logger.warning("Время жизни токена истекло.")
        else:
            logger.warning("Access не найден в Redis.")

        refresh_token = await self._redis_service.get_refresh_token("refresh_token")
        if refresh_token is None:
            logger.warning("Access токена нет! нужно пройти авторизацию")
            return None

        data = await self.refresh_token(method, refresh_token, headers)

        """ Сохраняем токены в кэш """
        await self._redis_service.save_access_token(
            key, data["access_token"], data["expires_in_access"]
        )
        await self._redis_service.save_refresh_token(
            "refresh_token", data["refresh_token"], data["expires_in_refresh"]
        )
        return data["access_token"]


async def get_post_response(redis_client: RedisService) -> dict[str, str | int]:
    user_data: dict[str, str] = get_user_config()
    headers: dict[str, str] = get_post_headers()

    async with HTTPClient() as http_client:
        auth = AuthService(redis_client, http_client)
        return await auth.authorization("POST", user_data, headers)
