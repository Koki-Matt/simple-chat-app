"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict  # pylint: disable=import-error


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and .env file."""

    app_name: str = "Simple Chat Backend"
    cors_origins: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")


settings = Settings()


