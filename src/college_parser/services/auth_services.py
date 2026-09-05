
import httpx

from src.college_parser.configs.user_config import config_user, get_user_config
from src.college_parser.headers.post_headers import get_post_headers
from src.college_parser.services.redis_service import RedisService
from src.college_parser.utils.logger import logger


class AuthService:
    def __init__(
        self,
        redis_service: RedisService,
        timeout: float = 30.0,
        max_connection: int = 100,
        max_keepalive_connection: int = 20,
    ) -> None:
        self._redis_service = redis_service
        self.timeout = timeout
        self.max_connection = max_connection
        self.max_keepalive_connection = max_keepalive_connection

        self.limits = httpx.Limits(
            max_keepalive_connections=max_keepalive_connection,
            max_connections=self.max_connection,
        )

        self.auth_url: str = str(config_user.AUTH_URL)
        self.get_url: str = str(config_user.BASE_URL)
        self._client: httpx.AsyncClient | None = None

    async def _get_connection(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=self.timeout,
                limits=self.limits,
                headers={"Accept": "application/json, text/plain, */*"},
            )
            return self._client
        return self._client

    # method for open connection
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
        user_data: dict[str, str],
        headers: dict[str, str],
    ) -> dict[str, str | int]:
        client = await self._get_connection()
        try:
            response = await client.post(self.auth_url, json=user_data, headers=headers)
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
                logger.error("Неверны логин или пароль.")
            else:
                logger.error(f"API вернул ошибку: {error}")
            raise
        else:
            return response.json()

    async def refresh_token(
        self, refresh_token: str, headers: dict[str, str]
    ) -> dict[str, str | int]:
        """Метод обновления refresh токена"""
        data: dict[str, str] = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        client = await self._get_connection()
        try:
            response = await client.post(self.auth_url, data=data, headers=headers)
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
        self, key: str, headers: dict[str, str]
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

        data = await self.refresh_token(refresh_token, headers)

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
    async with AuthService(redis_client) as auth_service:
        return await auth_service.authorization(user_data, headers)
