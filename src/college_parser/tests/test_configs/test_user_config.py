import os

import pytest
from dotenv import load_dotenv

from src.college_parser.configs.user_config import config_user

load_dotenv()

class TestValidConfig:
    """
    Тестирование валидного пользовательского конфига
    """
    @pytest.fixture
    def get_env_data(self) -> dict[str, str]:
        """
        Подготавливаем данные из .env для тестов"""
        return {
            'username': os.getenv("JOURNAL_NAME"),
            'password': os.getenv("JOURNAL_PASSWORD"),
            'application_key': os.getenv('APP_KEY'),
            'auth_url': os.getenv('AUTH_URL'),
            'base_url': os.getenv('BASE_URL')
        }

    def test_username(self, get_env_data) -> None:
        assert config_user.JOURNAL_NAME == get_env_data.get('username')
        assert config_user.JOURNAL_NAME is not None
        assert config_user.JOURNAL_NAME != ""
        assert len(config_user.JOURNAL_NAME) == len(get_env_data.get('username'))

    def test_password(self, get_env_data) -> None:
        assert config_user.JOURNAL_PASSWORD == get_env_data.get('password')
        assert config_user.JOURNAL_PASSWORD is not None
        assert config_user.JOURNAL_PASSWORD != ""
        assert len(config_user.JOURNAL_PASSWORD) == len(get_env_data.get('password'))

    def test_app_key(self, get_env_data) -> None:
        assert config_user.APP_KEY == get_env_data.get('application_key')
        assert config_user.APP_KEY is not None
        assert len(config_user.APP_KEY) > 20
        assert len(config_user.APP_KEY) == len(get_env_data.get("application_key"))

    def test_valid_urls(self, get_env_data) -> None:
        """Тестирование эндпоинта для авторизации
        """
        assert str(config_user.AUTH_URL) == get_env_data.get('auth_url')
        assert str(config_user.AUTH_URL) is not None
        assert len(str(config_user.AUTH_URL)) > 5
        assert str(config_user.AUTH_URL).startswith('https://')

        """
        Тестирование эндпоинта для парсинга
        """
        assert str(config_user.BASE_URL) == get_env_data.get('base_url')
        assert str(config_user.BASE_URL) is not None
        assert len(str(config_user.BASE_URL)) > 10
        assert str(config_user.BASE_URL).startswith('https://')