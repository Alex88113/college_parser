import os

import pytest
from dotenv import load_dotenv

from src.college_parser.configs.db_config import config_db, DBSettings

load_dotenv()


class TestSettingsDB:
    @pytest.fixture
    def get_data_db_from_env(self) -> dict[str, str | int]:
        return {
            'psql_username': os.getenv("PSQL_NAME"),
            'psql_password': os.getenv('PSQL_PASSWORD'),
            'psql_host': os.getenv("PSQL_HOST"),
            'psql_port': str(os.getenv('PSQL_PORT'))
        }

    @pytest.mark.parametrize("psql_name, psql_password, psql_host, psql_port, database", [
        ('postgres', 'mekfmkemf', 'localhost', 'o3ii34o3o', 'fmekfmkem'),
        ('postgres', '343fdfdf', 'localhost', 'fdlfmkdmfkdmfk', 'fdmfkdm'),
        ('postgres', '8394893849', True, 'localhost', 'fkmkemp23'),

        ('postgres', 'mdsmdksmd', 'kkoioe', 332323, 'lsalsl'),
        ('postgres', 'kldkldkw', 'dmdkwmd', 323, 'dsdklks')
])
    def test_db_config(
            self,
            monkeypatch,
            psql_name,
            psql_password,
            psql_host,
            psql_port,
            database):
        monkeypatch.setenv('PSQL_NAME', psql_name)
        monkeypatch.setenv("PSQL_PASSWORD", psql_password)
        monkeypatch.setenv('PSQL_HOST', psql_host)
        monkeypatch.setenv('PSQL_PORT', psql_port)
        monkeypatch.setenv('DATABASE', database)

        assert config_db.PSQL_NAME == psql_name

    def test_psql_name(self, get_data_db_from_env):
        assert config_db.PSQL_NAME == get_data_db_from_env.get('psql_username')
        assert config_db.PSQL_NAME is not None
        assert len(config_db.PSQL_NAME) == len(get_data_db_from_env.get('psql_username'))
        assert config_db.PSQL_NAME != ''

    def test_psql_password(self, get_data_db_from_env) -> None:
        assert config_db.PSQL_PASSWORD == get_data_db_from_env.get('psql_password')
        assert len(config_db.PSQL_PASSWORD) == len(get_data_db_from_env.get('psql_password'))
        assert config_db.PSQL_PASSWORD is not None
        assert config_db.PSQL_PASSWORD != ''

    def test_psql_host(self, get_data_db_from_env) -> None:
        assert config_db.PSQL_HOST == get_data_db_from_env.get('psql_host')
        assert len(config_db.PSQL_HOST) == len(get_data_db_from_env.get('psql_host'))
        assert config_db.PSQL_HOST is not None
        assert config_db.PSQL_HOST != ''

    def test_psql_port(self, get_data_db_from_env) -> None:
        print(type(config_db.PSQL_PORT))
        assert str(config_db.PSQL_PORT) == get_data_db_from_env.get('psql_port')
        assert len(str(config_db.PSQL_PORT)) == len(get_data_db_from_env.get('psql_port'))
        assert config_db.PSQL_PORT is not None
        assert config_db.PSQL_PORT != ""
        assert isinstance(config_db.PSQL_PORT, int)