from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl
from dotenv import load_dotenv

load_dotenv()

class DBSettings(BaseSettings):
    PSQL_NAME: str = Field(min_length=4)
    PSQL_PASSWORD: str = Field(min_length=4)
    PSQL_HOST: str = Field(min_length=4)
    PSQL_PORT: int = Field(ge=0)
    DATABASE: str = Field(min_length=5)

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        case_sensitive=True # ники переменных чувствительных к регистру
    )


config_db = DBSettings().model_dump()
