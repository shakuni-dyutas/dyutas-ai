from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_model_name: str
    openai_api_key: str

    langsmith_tracing: str = "false"
    langsmith_api_key: str = ""
    langsmith_project: str = ""
    langsmith_endpoint: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
