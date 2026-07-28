from redis.asyncio import Redis
import redis.asyncio as redis
from loguru import logger

from src.college_parser.configs.redis_config import redis_config_settings
from src.college_parser.models.redis_settings_shame import redis_settings

class RedisService:
    def __init__(self) -> None:
        self._ttl = redis_settings.ttl
        self._max_connections = redis_settings.max_connections
        self._decode_responses = redis_settings.decode_responses
        self._socket_timeout = redis_settings.socket_timeout
        self._socket_connect_timeout = redis_settings.socket_connect_timeout

        self._host = redis_config_settings.REDIS_HOST
        self._port = redis_config_settings.REDIS_PORT
        self._db = redis_config_settings.REDIS_DB
        self._password = redis_config_settings.REDIS_PASSWORD,
        self._username = redis_config_settings.REDIS_USER

        self._redis_client: Redis | None = None

    async def create_pool(self) -> Redis:
        if self._redis_client is None:
            pool = redis.ConnectionPool(
                port=self._port,
                host=self._host,
                decode_responses=self._decode_responses,
                max_connections=self._max_connections
            )
            self._redis_client = redis.Redis(connection_pool=pool)

            if await self._redis_client.ping():
                return self._redis_client

        return self._redis_client

    async def get_client(self) -> Redis:
        return self._redis_client

    async def close(self) -> None:
        if self._redis_client:
            await self._redis_client.aclose()
            self._redis_client = None

    async def check_connection(self) -> None:
        client = await self.create_pool()
        if await client.ping():
            logger.info("Подключение к бд установлено")
            logger.debug(f'БД работает на порту={self._port}, host={self._host}')
        else:
            logger.warning("Не удалось подключиться к Redis.")

    async def save_access_token(self, key: str, value: str, ttl: int) -> None:
        client = await self.get_client()
        await client.setex(key, ttl, value)
        logger.info(f"Access токен сохранён. TTL: {ttl} сек.")

    async def save_refresh_token(self, key: str, value: str, ttl: int) -> None:
        client = await self.get_client()
        await client.setex(key, ttl, value)
        logger.info(f"Refresh токен сохранён. TTL: {ttl} сек.")

    async def get_refresh_token(self, key: str) -> str | None:
        client = await self.get_client()
        if await client.exists(key):
            return await client.get(key)
        logger.warning('Refresh токена в кэше нет.')
        return None

    async def get_access_token(self, key: str) -> str | None:
        client = await self.get_client()
        if await client.exists(key):
            return await client.get(key)
        return None

    async def exists(self, key: str) -> bool:
        client = await self.get_client()
        if await client.exists(key):
            ttl_value: int = await client.ttl(key)
            logger.info(f"Токен есть в кэше.\nВремя жизни TTL: {ttl_value} сек.")
            return True
        else:
            logger.warning("Токена в кэше нет!")
            return False