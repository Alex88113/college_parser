import asyncio

import redis.asyncio as redis

from src.college_parser.services.auth_services import get_post_response
from src.college_parser.services.redis_service import RedisService
from src.college_parser.utils.logger import logger
from src.college_parser.utils.validation_post_response import get_valid_post_response


async def main() -> None:
    redis_client = RedisService()
    try:
        await redis_client.create_pool()
        await redis_client.check_connection()
    except redis.ConnectionError:
        logger.error("Не удалось установить соединение с Redis.")
        raise
    else:
        post_data = await get_post_response(redis_client)  # функция из авторизации
        result_valid = get_valid_post_response(post_data)  # валидация
        await redis_client.save_access_token(
            "access_token", result_valid.access_token, result_valid.expires_in_access
        )
        await redis_client.save_refresh_token(
            "refresh_token", result_valid.refresh_token, result_valid.expires_in_refresh
        )
        await redis_client.get_access_token("access_token")
        await redis_client.get_refresh_token("refresh_token")

        print(f"Есть ли access token?: {await redis_client.exists('access_token')}")
        print(f"Есть ли refresh token?: {await redis_client.exists('refresh_token')}")
    finally:
        await redis_client.close()


if __name__ == "__main__":
    asyncio.run(main())
