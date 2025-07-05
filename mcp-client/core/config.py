from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    slack_token: str
    google_client_secret: str
    mcp_server_uri: str
    google_redirect_uri: str
    groq_api_key: str
    class Config:
        env_file = ".env"

settings = Settings()
