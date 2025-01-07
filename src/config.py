import pathlib
from datetime import timedelta
from typing import List

from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseConfig(BaseModel):
    database_url: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20


class RedisConfig(BaseModel):
    redis_host: str
    redis_port: int
    redis_db: int
    state_ttl: timedelta = timedelta(weeks=2)
    data_ttl: timedelta = timedelta(weeks=2)


class AdminConfig(BaseModel):
    secret_key: str
    project_name: str


class BotConfig(BaseModel):
    bot_token: SecretStr


class ApiClientConfig(BaseModel):
    some_api_url: str
    some_other_api_url: str


class ServerConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    forwarded_allow_ips: list[str] = ["*"]


class ApiConfig(BaseModel):
    project_name: str = "Base Project"
    project_version: str = "0.0.0"


class LogConfig(BaseModel):
    log_bot_token: SecretStr
    maintainers_user_ids: List[int]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{pathlib.Path(__file__).parents[1]}/.env",
        extra="ignore",
    )

    # PostgreSQL database settings
    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_password: str
    postgres_user: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    # Redis settings
    redis_host: str
    redis_port: int
    redis_db: int

    # API client settings
    some_api_url: str
    some_other_api_url: str

    # Bot settings
    bot_token: str

    # Logging settings
    log_bot_token: str
    maintainers_user_ids: List[int] = Field(default_factory=list)

    # Security settings
    secret_key: str
    forwarded_allow_ips: list[str]

    # S3 settings
    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    s3_endpoint_url: str
    s3_domain: str

    # Server settings
    server_host: str
    server_port: int

    @property
    def redis_config(self) -> RedisConfig:
        """Возвращает объект конфигурации Redis."""
        return RedisConfig(
            redis_host=self.redis_host,
            redis_port=self.redis_port,
            redis_db=self.redis_db,
        )

    @property
    def database_config(self) -> DatabaseConfig:
        """Возвращает объект конфигурации базы данных."""
        return DatabaseConfig(
            database_url=self.database_url,
        )

    @property
    def api_client_config(self) -> ApiClientConfig:
        """Возвращает объект конфигурации клиента."""
        return ApiClientConfig(
            some_api_url=self.some_api_url,
            some_other_api_url=self.some_other_api_url,
        )

    @property
    def bot_config(self) -> BotConfig:
        """Возвращает объект конфигурации бота."""
        return BotConfig(
            bot_token=self.bot_token,
        )

    @property
    def server_config(self) -> ServerConfig:
        """Возвращает объект конфигурации сервера."""
        return ServerConfig(
            host=self.server_host,
            port=self.server_port,
            forwarded_allow_ips=self.forwarded_allow_ips,
        )

    @property
    def api_config(self) -> ApiConfig:
        """Возвращает объект конфигурации api."""
        return ApiConfig()

    @property
    def admin_config(self) -> AdminConfig:
        """Возвращает объект конфигурации админки."""
        return AdminConfig(
            project_name=self.api_config.project_name,
            secret_key=self.secret_key,
        )

    @property
    def log_config(self) -> LogConfig:
        """Возвращает объект конфигурации логирования."""
        return LogConfig(
            log_bot_token=self.log_bot_token,
            maintainers_user_ids=self.maintainers_user_ids,
        )


settings = Settings()
