from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    database_url: str = "postgresql+asyncpg://matchvault:matchvault@localhost:5432/matchvault"
    secret_key: str = "dev-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    nomba_api_key: str = ""
    nomba_webhook_secret: str = ""
    api_football_key: str = ""
    frontend_url: str = "http://localhost:3000"


settings = Settings()
