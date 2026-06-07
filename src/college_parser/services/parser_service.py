from typing import List, Dict
import asyncio

import httpx

from src.college_parser.headers.headers_get import get_headers_request
from src.college_parser.services.auth_services import AuthService
from src.college_parser.configs.user_config import config_user

class Parsing:
    async def parsing_schedule(
            self,
            url: str,
            headers: Dict[str, str]
    ) -> List[Dict[str, str | int]]:

        async with AuthService() as auth_client:
            response = await auth_client.authorization.get(url, headers=headers)
            response.raise_for_status()
            return response.json()

async def get_parsing_data():
    parsing = Parsing()
    headers: dict[str, str] = await asyncio.create_task(get_headers_request())
    result = await asyncio.create_task(parsing.parsing_schedule(str(config_user.BASE_URL), headers))
    print(result)

asyncio.run(get_parsing_data())

