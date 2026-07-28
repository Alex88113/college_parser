import asyncio

from redis.asyncio import Redis
import redis.asyncio as redis
from loguru import logger

from src.college_parser.configs.redis_config import redis_config_settings
from src.college_parser.models.redis_settings_shame import redis_settings

class RedisService:
    def __init__(self) -> None:
        # Настройки пула
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

    async def init_pool(self) -> Redis:
        if self._redis_client is None:
            pool = redis.ConnectionPool(
                port=self._port,
                host=self._host,
                decode_responses=self._decode_responses,
                max_connections=self._max_connections
            )
            self._redis_client = redis.Redis(connection_pool=pool)
            if await self._redis_client.ping():
                logger.info("Подключение к бд установлено")
                return self._redis_client

        return self._redis_client

    async def close(self) -> None:
        if self._redis_client:
            await self._redis_client
            self._redis_client = None

async def main():
    redis_client = RedisService()
    try:
        await redis_client.init_pool()
    finally:
        await redis_client.close()

asyncio.run(main())