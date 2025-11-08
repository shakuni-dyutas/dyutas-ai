from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_model_name: str
    groq_api_key: str

    langsmith_tracing: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
