from pydantic_settings import BaseSettings


class WorkerSettings(BaseSettings):
    dispatch_url: str = "http://localhost:8000"

    hostname: str | None = None

    min_sleep: int = 1
    max_sleep: int = 3

    poll_interval: float = 1.0
    http_timeout: float = 10.0

    class Config:
        # env_file = ".dotenv"
        env_file_encoding = "utf-8"
        env_prefix = ""
        case_sensitive = False


settings = WorkerSettings()
