from typing import Any
import asyncio
from pydantic import ValidationError
from loguru import logger
from src.journal_project.services.parsing_service import get_parsing_data
from src.journal_project.models.lesson import GetResponse

class ValidGetResponse:
    def __init__(self, schedule: list[dict[str, Any]]) -> None:
        if not isinstance(schedule, list) or schedule == [] or schedule is None:
            raise ValueError("Для валидации требуется список со словарями")

        self.schedule = schedule
        self.schedule_valid = None

    async def _valid_schedule(self):
        self.schedule_valid = []
        try:
            for data in self.schedule:
                if data['date'] == '2026-05-19':
                    valid_schedule = GetResponse(**data).model_dump()
                    self.schedule_valid.append(valid_schedule)

        except ValidationError as error:
            raise ValidationError(f"Данные не валидны!\nПричина: {error}")

        return self.schedule_valid

async def get_valid_schedule() -> list[dict[str, Any]]:
    try:
        data = await get_parsing_data()
        valid_obj= ValidGetResponse(data)
        result = await valid_obj._valid_schedule()

    except ValueError as error:
        logger.error("Некорректно переданный аргумент для валидации GET response: {error}", error=error)
        raise

    except Exception as error:
        logger.error("Неизвестная ошибка: {error}", error=error)
        raise

    return result

