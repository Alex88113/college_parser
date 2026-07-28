from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class RedisConfig(BaseSettings):
    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_DB: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

redis_config_settings = RedisConfig()
