from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class CouchbaseSettings(BaseSettings):
    """Connection configuration; add the SDK with the first real repository."""

    model_config = SettingsConfigDict(
        env_prefix="COUCHBASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    connection_string: str = "couchbase://localhost"
    username: str = "Administrator"
    password: SecretStr = SecretStr("password")
    bucket: str = "app"
