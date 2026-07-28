import asyncio

from loguru import logger

from src.college_parser.utils.validation_get_response import get_valid_schedule
from src.college_parser.utils.validation_post_response import get_refresh_token


async def get_schedule_today(group: str = "РПО-3") -> str:
    """Получить расписание на сегодня для группы"""
    # Получаем токен для авторизации (если нужен)
    token = await get_refresh_token()

    # Парсим расписание
    schedule = await get_valid_schedule(group, "today", token)

    # Форматируем для вывода в HTML
    if isinstance(schedule, str):
        return schedule
    elif isinstance(schedule, list):
        if not schedule:
            return "📭 На сегодня пар нет."

        lines = []
        for lesson in schedule:
            time = lesson.get("time", "")
            name = lesson.get("name", "")
            teacher = lesson.get("teacher", "")
            room = lesson.get("room", "")

            line = f"🕐 {time} | {name}"
            if teacher:
                line += f" | 👨‍🏫 {teacher}"
            if room:
                line += f" | 📍 {room}"
            lines.append(line)
        return "\n".join(lines)
    else:
        return "⚠️ Не удалось получить расписание."
