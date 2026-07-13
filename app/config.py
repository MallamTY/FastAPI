from pydantic_settings import BaseSettings



class Settings(BaseSettings):
    database_username: str
    database_password: str
    database_name: str
    database_hostname: str
    database_port: str
    secret_key: str
    algorithm: str
    expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings()