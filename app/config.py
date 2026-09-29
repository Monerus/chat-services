from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):

    PUBLIC_KEY_PATH: Path = BASE_DIR / "keys" / "public.pem"

    POSTGRES_CONNECT: str
    JWT_ALGORITHM: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()