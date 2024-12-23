import pathlib
from typing import List

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f"{pathlib.Path(__file__).parents[1]}/.env",
        extra="ignore",
    )

    postgres_host: str
    postgres_port: str
    postgres_db: str
    postgres_password: str
    postgres_user: str
    db_echo: bool = False

    redis_host: str
    redis_port: int
    redis_db: int

    api_url: str
    bot_token: SecretStr
    log_bot_token: SecretStr
    maintainers_user_ids: List[int] = Field(default_factory=list)

    secret_key: str
    forwarded_allow_ips: list[str] = ["*"]

    aws_access_key_id: str
    aws_secret_access_key: str
    s3_bucket: str
    s3_endpoint_url: str
    s3_domain: str

    project_name: str = "Base Project"
    project_version: str = "0.0.0"

    @property
    def database_url(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def base_url(self):
        return f"{self.api_url}/api"


settings = Settings()
