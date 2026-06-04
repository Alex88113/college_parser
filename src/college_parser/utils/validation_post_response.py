import asyncio
from typing import Dict, Any

from pydantic import ValidationError
from loguru import logger

logger.debug("Начало импорта модуля авторизации....")

try:
    from src.journal_project.models.post_response import PostAnswer
    from src.journal_project.services.auth_service import get_post_response
    logger.success("Импорт прошел успешно!")

except ModuleNotFoundError as error:
    logger.error("Модуль с таким именем не найден.\nПричина: {error}", error=error)
    raise

except ImportError as error:
    logger.error("При импорте пользовательского конфига возникла ошибка: {error}", error=error)
    raise

class ValidPostAnswer:
    def __init__(self, data: Dict[str, Any]) -> None:
        if not isinstance(data, dict) or data == {}:
            raise ValueError("Переданный объект либо не является json либо он пуст")

        self.data = data

    async def validation_post_answer(self) -> str | None:
        try:
            valid_data = PostAnswer(**self.data)

        except ValidationError as error:
            raise ValidationError(f'Невалидные данные: {error}') from error

        return valid_data.refresh_token

async def get_valid_token() -> str:
    try:
        post_answer = await get_post_response()
        valid_obj = ValidPostAnswer(post_answer)
        result = await valid_obj.validation_post_answer()

    except ValueError as error:
        logger.error("Некорректно переданные данные для валидации: {error}", error=error)
        raise
    except Exception as error:
        logger.error("Возникла непредвиденная ошибка: {error}", error=error)
        raise

    return result
