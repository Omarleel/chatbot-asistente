from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    slack_token: str
    google_client_secret: str
    class Config:
        env_file = ".env"

settings = Settings()
