from pydantic import ValidationError

from src.college_parser.models.post_response import PostAnswer


class ValidPostResponse:
    def __init__(self, post_response: dict[str, str | int]) -> None:
        self.post_response = post_response
        self._valid_post_answer: PostAnswer | None = None

    def _validation_response(self) -> PostAnswer:
        try:
            valid_data: PostAnswer = PostAnswer(**self.post_response)
            self._valid_post_answer = valid_data
            return self._valid_post_answer
        except ValidationError as error:
            raise ValidationError(
                f"Возникла ошибка при валидации пост ответ: {error}"
            ) from error

    def get_valid_response(self) -> PostAnswer:
        self._validation_response()
        return self._valid_post_answer


def get_valid_post_response(post_data: dict[str, str | int]) -> PostAnswer:
    try:
        valid_post = ValidPostResponse(post_data)
        result_valid = valid_post.get_valid_response()
    except ValueError as error:
        raise ValueError(f"Проблемы с переданным refresh token: {error}") from error
    else:
        return result_valid
