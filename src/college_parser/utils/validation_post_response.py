from pydantic import ValidationError

from src.college_parser.models.post_response import PostAnswer
from src.college_parser.services.auth_services import get_post_response

class ValidPostResponse:
    def __init__(self, post_response: dict[str, str | int]) -> None:
        self.post_response = post_response
        self.valid_post_answer: PostAnswer | None = None
        self.refresh_token: str | None = None


    def _validation_response(self) -> PostAnswer:
        try:
            valid_data: PostAnswer = PostAnswer(**self.post_response)
            self.valid_post_answer = valid_data
            self.refresh_token = valid_data.refresh_token
            return self.valid_post_answer
        except ValidationError as error:
            raise ValidationError(f'Возникла ошибка при валидации пост ответ: {error}') from error

    def get_valid_refresh_token(self) -> str:
        self._validation_response()
        if self.refresh_token is None:
            raise ValueError("Токен не прошел валидацию")
        else:
            return self.refresh_token

async def get_refresh_token() -> str:
    post_data = await get_post_response()
    try:
        valid_post = ValidPostResponse(post_data)
        result_valid: str = valid_post.get_valid_refresh_token()
        return result_valid
    except ValueError as error:
        raise ValueError(f"Проблемы с переданным refresh token: {error}") from error