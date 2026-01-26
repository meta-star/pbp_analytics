import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    PORT: int = 2020
    ENV: str = "production"

    # MySQL
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "pbp_analytics"

    # Services
    SAFE_BROWSING_API_KEY: str = ""
    PHISHTANK_USERNAME: str = ""
    PHISHTANK_API_KEY: str = ""

    # WebCapture
    CAPTURE_BROWSER: str = "firefox" # or chrome
    CAPTURE_TYPE: str = "2" # 1: BrowserRender, 2: BrowserAgent
    CACHE_PATH: str = "cache/"

    # Torch Device
    # "cpu", "cuda", "mps", or "auto"
    TORCH_DEVICE: str = "auto"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return f"mysql+aiomysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

settings = Settings()
