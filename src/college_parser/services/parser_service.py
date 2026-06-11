from typing import List, Dict
import asyncio

import httpx

from src.college_parser.headers.headers_get import get_headers_request
from src.college_parser.configs.user_config import config_user

class Parsing:
    async def parsing_schedule(
            self,
            url: str,
            headers: Dict[str, str]
    ) -> List[Dict[str, str | int]]:

        async with httpx.AsyncClient() as auth_client:
            response = await auth_client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

async def get_parsing_data() -> List[Dict[str, str | int]]:
    parsing: Parsing = Parsing()
    headers: dict[str, str] = await asyncio.create_task(get_headers_request())
    result = await parsing.parsing_schedule(str(config_user.BASE_URL), headers)
    return result

