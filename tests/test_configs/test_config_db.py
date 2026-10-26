import os

import pytest
from dotenv import load_dotenv

from src.college_parser.configs.db_config import config_db

load_dotenv()


class TestSettingsDB:
    @pytest.fixture
    def get_data_db_from_env(self) -> dict[str, str | int]:
        return {
            "psql_username": os.getenv("PSQL_NAME"),
            "psql_password": os.getenv("PSQL_PASSWORD"),
            "psql_host": os.getenv("PSQL_HOST"),
            "psql_port": str(os.getenv("PSQL_PORT")),
        }

    def test_psql_name(self, get_data_db_from_env):
        assert get_data_db_from_env.get("psql_username") == config_db.PSQL_NAME
        assert config_db.PSQL_NAME is not None
        assert len(config_db.PSQL_NAME) == len(
            get_data_db_from_env.get("psql_username")
        )
        assert config_db.PSQL_NAME != ""

    def test_psql_password(self, get_data_db_from_env) -> None:
        assert get_data_db_from_env.get("psql_password") == config_db.PSQL_PASSWORD
        assert len(config_db.PSQL_PASSWORD) == len(
            get_data_db_from_env.get("psql_password")
        )
        assert config_db.PSQL_PASSWORD is not None
        assert config_db.PSQL_PASSWORD != ""

    def test_psql_host(self, get_data_db_from_env) -> None:
        assert get_data_db_from_env.get("psql_host") == config_db.PSQL_HOST
        assert len(config_db.PSQL_HOST) == len(get_data_db_from_env.get("psql_host"))
        assert config_db.PSQL_HOST is not None
        assert config_db.PSQL_HOST != ""

    def test_psql_port(self, get_data_db_from_env) -> None:
        print(type(config_db.PSQL_PORT))
        assert str(config_db.PSQL_PORT) == get_data_db_from_env.get("psql_port")
        assert len(str(config_db.PSQL_PORT)) == len(
            get_data_db_from_env.get("psql_port")
        )
        assert config_db.PSQL_PORT is not None
        assert config_db.PSQL_PORT != ""
        assert isinstance(config_db.PSQL_PORT, int)
