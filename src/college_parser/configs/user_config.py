from typing import Dict
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, HttpUrl
from dotenv import load_dotenv

load_dotenv()

class UserSettings(BaseSettings):
    JOURNAL_NAME: str = Field(min_length=5)
    JOURNAL_PASSWORD: str = Field(min_length=5)
    APP_KEY: str = Field(min_length=5)
    AUTH_URL: HttpUrl
    BASE_URL: HttpUrl

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore', # игнорировать лишние переменные в .env
        case_sensitive=True
    )

config_user = UserSettings()

def get_user_config() -> Dict[str, str]:
    return {
        'username': config_user.JOURNAL_NAME,
        'password': config_user.JOURNAL_PASSWORD,
        'application_key': config_user.APP_KEY
    }



