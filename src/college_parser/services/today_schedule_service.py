
from src.college_parser.utils.validation_get_response import get_valid_schedule_default


class TodaySchedule:
    @staticmethod
    def _formatted_schedule_today(schedule_data: list[dict[str, str | int]]) -> str:
        """Форматирует расписание для вывода"""
        if not schedule_data:
            return "Расписание отсутствует"

        schedule: list[str] = []
        for data in schedule_data:
            schedule.append(
                f"📚Пара: {data.get('subject_name')} |👨‍🏫 Преподаватель: {data.get('teacher_name')}"
            )
            schedule.append(
                f"🕐Начало {data.get('started_at')} | 🏁 Конец {data.get('finished_at')}"
            )
            schedule.append(f"🏛️Аудитория: {data.get('room_name')}")
            schedule.append(
                "----------------------------------------------------------------------"
            )

        return "\n".join(schedule)

    @staticmethod
    def format_schedule(data: list[dict[str, str | int]]) -> str:
        body = TodaySchedule._formatted_schedule_today(data)
        return body


async def get_schedule_today() -> str:
    """Получаем готовое отформатированное расписание на сегодня"""
    data = await get_valid_schedule_default()
    return TodaySchedule.format_schedule(data)
