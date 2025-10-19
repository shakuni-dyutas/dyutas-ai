from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    groq_model_name: str
    groq_api_key: str

    langsmith_tracing: bool = False
    langsmith_api_key: str = ""
    langsmith_project: str = ""

    class Config:
        env_file = ".env"
