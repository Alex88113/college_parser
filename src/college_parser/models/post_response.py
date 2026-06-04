from pydantic import Field, BaseModel

class PostAnswer(BaseModel):
    refresh_token: str = Field(min_length=30)
    access_token: str = Field(min_length=30)
    expires_in_refresh: int = Field(ge=0)
    expires_in_access: int = Field(ge=0)