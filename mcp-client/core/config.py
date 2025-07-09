from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    mongodb_uri: str
    qdrant_host: str
    qdrant_port: str
    qdrant_collection: str
    slack_client_id: str
    slack_client_secret: str
    slack_redirect_uri: str
    google_client_secret: str
    mcp_server_uri: str
    google_redirect_uri: str
    groq_api_key: str
    class Config:
        env_file = ".env"

settings = Settings()
