from typing import List, Dict, Optional
from pydantic import ValidationError
import asyncio
from datetime import datetime

from src.college_parser.services.parser_service import get_parsing_data
from src.college_parser.models.lesson import GetResponse


class ValidGetResponse:
    """
    Валидатор и форматер дат и расписания
    """

    def __init__(self, parsing_data: List[Dict[str, str | int]]) -> None:
        if not isinstance(parsing_data, list):
            raise ValueError("Требуется список с данными")
        if not parsing_data:
            raise ValueError("Список с данными пуст")

        self.parsing_data = parsing_data
        self._valid_schedule: List[Dict] | None = None  # 👈 храним словари

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
    def _formater_date_today() -> str:
        today = datetime.now()
        return today.strftime("%Y-%m-%d")

    @staticmethod
    def _formater_schedule(valid_schedule: List[Dict]) -> str:
        """Форматирует расписание для вывода"""
        lines = ['\n']
        today = ValidGetResponse._formater_date_today()

        for data in valid_schedule:
            if data.get('date') == '2026-06-11':
                lines.append(f"📚Пара: {data.get('subject_name')} |👨‍🏫 Преподаватель: {data.get('teacher_name')}")
                lines.append(f"🕐Начало {data.get('started_at')} | 🏁 Конец {data.get('finished_at')}")
                lines.append(f"🏛️Аудитория: {data.get('room_name')}")
                lines.append("----------------------------------------------------------------------")

        return "\n".join(lines)

    def get_ready_schedule(self) -> str:
        """Главный метод для получения готового расписания"""
        valid_data = self._validation_parsing_data(self.parsing_data)
        # Форматируем и возвращаем
        return self._formater_schedule(valid_data)


async def get_schedule_today() -> str:
    """Получает расписание на сегодня"""
    parsing_data: List[Dict[str, str | int]] = await get_parsing_data()
    try:
        valid_obj: ValidGetResponse = ValidGetResponse(parsing_data)
        result = valid_obj.get_ready_schedule()
        return result
    except ValueError as error:
        raise ValueError(f"Некорректно переданный аргумент: {error}") from error
