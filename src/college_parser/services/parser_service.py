from typing import Dict, List

import httpx
from httpx import Response

from src.college_parser.services.get_tokens_service import get_tokens
from src.college_parser.configs.user_config import config_user
from src.college_parser.utils.logger import *

class ParsingService:
    def __init__(self) -> None:
        self._url: str = str(config_user.BASE_URL)

    @staticmethod
    def _request_get_headers(token: str) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "ru_RU, ru",
            "authorization": f"Bearer {token}",
            "origin": "https://journal.top-academy.ru",
            "referer": "https://journal.top-academy.ru/",
            "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "YaBrowser";v="26.4", "Yowser";v="2.5"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 YaBrowser/26.4.0.0 Safari/537.36"
        }

    async def _parsing_schedule(self, token: str) -> Response | None:
        headers = ParsingService()._request_get_headers(token)
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(self._url, headers=headers)
                response.raise_for_status()
            except httpx.HTTPStatusError as error:
                if error.response.status_code == 401:
                    logger.error(f"Не удалось пройти авторизацию по эндпоинту: {response.url}."
                    f"\nПричина: {error.response.text}, {error.response}")
                    raise
                elif error.response.status_code == 403:
                    logger.error(f'Запрашиваемый ресурс по {response.url} не найден.\nПричина: {error}')
                    raise
            else:
                return response

    async def get_parsing_data(self, token: str) -> List[Dict[str, str | int]] | None:
        data = await self._parsing_schedule(token)
        if data:
            return data.json()
        return None

async def get_parsing_schedule() -> List[Dict[str, str | int]] | None:
    token = await get_tokens()
    logger.info(f'Token from cache: {token}')
    parsing = ParsingService()
    result_parsing = await parsing.get_parsing_data(token['access_token'])
    if result_parsing:
        return result_parsing
    else:
        logger.info("Данных нет.")
        return  None
