import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(str, enum.Enum):  # noqa: WPS600
    """Возможные уровни логирования."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Настройки бота.

    Доступ к настройкам можно получить из виртуального окружения.
    """

    log_level: LogLevel = LogLevel.INFO

    # Настройки Базы Данных.
    db_host: str = "farpostbooks_backend"
    db_port: int = 5432
    db_user: str = "farpostbooks_backend"
    db_pass: str = "farpostbooks_backend"
    db_base: str = "farpostbooks_backend"
    db_echo: bool = False

    # Конфигурация для Telegram
    bot_token: str = "42:TOKEN"

    # Настройки Redis'а.
    redis_host: str = "redis"
    redis_port: int = 6379

    @property
    def db_url(self) -> URL:
        """
        Сборка ссылки на основе настроек для доступа к Базе Данных.

        :return: URL базы данных.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "FARPOSTBOOKS_TELEGRAM_"
        env_file_encoding = "utf-8"


settings = Settings()
