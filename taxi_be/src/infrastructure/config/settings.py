from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    hostname: str = "taxi_dispatcher"
    min_pos_x: int = 1
    max_pos_x: int = 100
    min_pos_y: int = 1
    max_pos_y: int = 100
    # this is for local use only, never store secrets in the repo, sslmode should be added at the end of conn string
    # https://www.postgresql.org/docs/current/libpq-ssl.html
    db_conn_string: str = f"postgresql+asyncpg://usr:S0S1rongPsw@localhost:15432/taxi_db"

    class Config:
        # env_file = ".dotenv"
        env_file_encoding = "utf-8"
        env_prefix = ""
        case_sensitive = False


settings = AppSettings()
