import asyncio
from typing import Dict, List
from datetime import datetime, timedelta

from src.college_parser.utils.validation_get_response import get_valid_schedule

class TomorrowService:
    def __init__(self) -> None:
        self.tomorrow_schedule: str | None = None

    @staticmethod
    def _formatter_tomorrow_date() -> str:
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        return tomorrow.strftime('%Y-%m-%d')

    @staticmethod
    def _formatter_tomorrow_schedule(schedule_today: List[Dict[str, str | int]]) -> str:
        """Форматирует расписание для вывода"""
        lines = ['\n']
        today = TomorrowService._formatter_tomorrow_date()

        for data in schedule_today:
            if data.get('date') == today:
                lines.append(f"📚Пара: {data.get('subject_name')} |👨‍🏫 Преподаватель: {data.get('teacher_name')}")
                lines.append(f"🕐Начало {data.get('started_at')} | 🏁 Конец {data.get('finished_at')}")
                lines.append(f"🏛️Аудитория: {data.get('room_name')}")
                lines.append("----------------------------------------------------------------------")

        return "\n".join(lines)

    def get_formatter_schedule_tomorrow(self, tomorrow) -> str:
        tomorrow_schedule = TomorrowService._formatter_tomorrow_schedule(tomorrow)
        self.tomorrow_schedule = tomorrow_schedule
        return self.tomorrow_schedule

async def get_tomorrow_schedule() -> str:
    try:
        valid_data = await get_valid_schedule()
        tomorrow_service = TomorrowService()
        get_tomorrow = tomorrow_service.get_formatter_schedule_tomorrow(valid_data)

        print(get_tomorrow)
        return get_tomorrow

    except ValueError as error:
        raise ValueError(f'Возникли проблемы с: {error}') from error

    except Exception as error:
        raise Exception(f'Возникла неизвестная ошибка: {error}')

