import asyncio
import redis.asyncio as redis

from src.college_parser.utils.validation_post_response import get_valid_post_response
from src.college_parser.services.redis_service import RedisService
from src.college_parser.services.auth_services import get_post_response
from src.college_parser.utils.logger import *

async def get_tokens() -> dict[str, str]:
    redis_client = RedisService()
    try:
        await redis_client.create_pool()
        await redis_client.check_connection()
    except redis.ConnectionError as error:
        logger.error(f'Не удалось установить соединение с Redis.\nПричина: {error}')
        raise
    else:
        post_data = await get_post_response(redis_client)
        result_valid = get_valid_post_response(post_data)
        await redis_client.save_access_token(
            'access_token',
            result_valid.access_token,
            result_valid.expires_in_access
        )
        await redis_client.save_refresh_token(
            'refresh_token',
            result_valid.refresh_token,
            result_valid.expires_in_refresh
        )
        return {
            'access_token': await redis_client.get_access_token("access_token"),
            'refresh_token': await redis_client.get_refresh_token('refresh_token')
        }
