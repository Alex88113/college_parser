import asyncio
from pydantic import ValidationError

from src.college_parser.models.post_response import PostAnswer
from src.college_parser.services.auth_services import get_post_response

class ValidPostResponse:
    def __init__(self, post_response: dict[str, str | int]) -> None:
        init_post_response = post_response
        if not isinstance(init_post_response, dict):
            raise ValueError(f"""
            Переданный объект post request некорректен.
            Тип переданного объекта: {type(post_response)}""")

        if init_post_response == {}:
            raise ValueError("словарь ответа post запроса пуст")

        self.post_response = init_post_response
        self.refresh_token: str | None = None
        self.valid_post_answer = None

    def _validation_response(self) -> dict[str, str | int]:
        try:
            valid_data: PostAnswer = PostAnswer(**self.post_response)
            transformation_valid_data = valid_data.model_dump()
            self.valid_post_answer = transformation_valid_data
            self.refresh_token = transformation_valid_data.get('refresh_token')
            return self.valid_post_answer
        except ValidationError as error:
            raise ValidationError(f'Возникла ошибка при валидации пост ответ: {error}')

    def get_valid_data(self) -> str | None:
        if self._validation_response() is not None:
            return self.refresh_token
        else:
            print("Валидных данных нет")

async def get_refresh_token() -> str:
    post_data = await get_post_response()
    valid_post = ValidPostResponse(post_data)
    result_valid: str | None = valid_post.get_valid_data()
    return result_valid