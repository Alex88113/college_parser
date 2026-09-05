from pydantic import BaseModel, Field


class GetResponse(BaseModel):
    date: str
    lesson: int = Field(ge=0)
    started_at: str
    finished_at: str
    teacher_name: str = Field(min_length=4, max_length=100)
    subject_name: str = Field(min_length=4, max_length=200)
    room_name: str = Field(min_length=4, max_length=20)
