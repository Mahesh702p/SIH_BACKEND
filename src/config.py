from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "your_super_secret_key_that_should_be_long_and_random"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AGORA_APP_ID: str | None = None
    AGORA_APP_CERTIFICATE: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()