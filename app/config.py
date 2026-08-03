from pydantic import ConfigDict
from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_name: str
    database_hostname: str
    test_database_name: str
    database_port: str
    secret_key: str
    algorithm: str
    expire_minutes: int

    model_config = ConfigDict(env_file=".env")


settings = Settings()