import asyncio
from typing import Dict, List
from datetime import datetime

from src.college_parser.utils.validation_get_response import get_valid_schedule

class TodayService:
    def __init__(self) -> None:
        self.schedule_today: str | None =  None

    @staticmethod
    def _formatter_today_date() -> str:
        today = datetime.now()
        formatter_date = today.strftime("%Y-%m-%d")
        return formatter_date

    @staticmethod
    def _formatter_today_schedule(schedule_today: List[Dict[str, str | int]]) -> str:
        """Форматирует расписание для вывода"""
        lines = ['\n']
        today = TodayService._formatter_today_date()

        for data in schedule_today:
            if data.get('date') == today:
                lines.append(f"📚Пара: {data.get('subject_name')} |👨‍🏫 Преподаватель: {data.get('teacher_name')}")
                lines.append(f"🕐Начало {data.get('started_at')} | 🏁 Конец {data.get('finished_at')}")
                lines.append(f"🏛️Аудитория: {data.get('room_name')}")
                lines.append("----------------------------------------------------------------------")

        return "\n".join(lines)

    def get_formatter_schedule(self, schedule) -> str:
        formatter_schedule = TodayService._formatter_today_schedule(schedule)
        self.schedule_today = formatter_schedule
        return self.schedule_today

async def get_schedule_today() -> str:
    try:
        valid_schedule = await get_valid_schedule()
        today_obj = TodayService()
        today_schedule = today_obj.get_formatter_schedule(valid_schedule)
        return today_schedule
    except ValueError as error:
        raise ValueError(f"Проблемы с: {error}") from error