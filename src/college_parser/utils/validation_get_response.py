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

async def get_valid_schedule() -> List[Dict[str, str | int]]:
    """ Получаем валидные данные """
    parsing_data: List[Dict[str, str | int]] = await get_parsing_data()
    try:
        result_valid = ValidGetResponse.get_valid_data(parsing_data)
        return result_valid
    except ValueError as error:
        raise ValueError(f"Некорректно переданный аргумент: {error}") from error
