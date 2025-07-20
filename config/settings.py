from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()
