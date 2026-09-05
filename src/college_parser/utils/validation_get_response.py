
from pydantic import ValidationError

from src.college_parser.models.lesson import GetResponse
from src.college_parser.services.parser_service import get_parsing_schedule


class ValidGetResponse:
    """
    Валидатор и форматер дат и расписания
    """

    @staticmethod
    def _validation_parsing_data(
        parsing_data: list[dict[str, str | int]],
    ) -> list[dict]:
        """Валидирует данные и возвращает список словарей"""
        lines = []
        for data in parsing_data:
            try:
                valid_data = GetResponse(**data).model_dump()
                lines.append(valid_data)
            except ValidationError as error:
                raise ValidationError(
                    f"Возникла ошибка при валидации данных расписания: {error}"
                ) from error
        return lines

    @staticmethod
    def get_valid_data(parsing_data) -> list:
        return ValidGetResponse._validation_parsing_data(parsing_data)


async def get_valid_schedule() -> list[dict[str, str | int]]:
    parsing_data: list[dict[str, str | int]] = await get_parsing_schedule()
    try:
        result_valid = ValidGetResponse.get_valid_data(parsing_data)
        return result_valid
    except ValueError as error:
        raise ValueError(f"Некорректно переданный аргумент: {error}") from error


async def get_valid_schedule_default() -> list[dict[str, str | int]]:
    """Получает валидные данные для группы РПО-3 на 10 июня 2026"""
    return await get_valid_schedule()
