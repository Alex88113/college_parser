from typing import List, Dict
import asyncio

from pydantic import ValidationError

from src.college_parser.services.parser_service import get_parsing_data
from src.college_parser.models.lesson import GetResponse


class ValidGetResponse:
    """
    Валидатор и форматер дат и расписания
    """

    @staticmethod
    def _validation_parsing_data(parsing_data: List[Dict[str, str | int]]) -> List[Dict]:
        """Валидирует данные и возвращает список словарей"""
        lines = []
        for data in parsing_data:
            try:
                valid_data = GetResponse(**data).model_dump()
                lines.append(valid_data)
            except ValidationError as error:
                raise ValidationError(f'Возникла ошибка при валидации данных расписания: {error}') from error
        return lines

    @staticmethod
    def get_valid_data(parsing_data) -> list:
        return ValidGetResponse._validation_parsing_data(parsing_data)


async def get_valid_schedule(group: str, day: str, token: str = None) -> List[Dict[str, str | int]]:
    """
    Получает валидные данные расписания для группы и дня

    Args:
        group: Название группы (например, "РПО-3")
        day: День ("today", "tomorrow" или дата в формате "2026-06-10")
        token: Токен авторизации (опционально)

    Returns:
        Список словарей с валидным расписанием
    """
    # Используем переданные группу и день
    parsing_data: List[Dict[str, str | int]] = await get_parsing_data(group, day)

    try:
        result_valid = ValidGetResponse.get_valid_data(parsing_data)
        return result_valid
    except ValueError as error:
        raise ValueError(f"Некорректно переданный аргумент: {error}") from error


# Для обратной совместимости (если кто-то вызывает без аргументов)
async def get_valid_schedule_default() -> List[Dict[str, str | int]]:
    """Получает валидные данные для группы РПО-3 на 10 июня 2026"""
    return await get_valid_schedule("РПО-3", "2026-06-10")