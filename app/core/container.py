from dependency_injector import containers, providers
from langchain_openai import ChatOpenAI

from app.core.config import Settings
from app.core.domains.judge.judge_service import JudgeService


class Container(containers.DeclarativeContainer):
    config: Settings = providers.Configuration(pydantic_settings=[Settings()])

    judge_model = providers.Singleton(
        ChatOpenAI,
        model=config.openai_model_name,
        api_key=config.openai_api_key,
    )

    judge_service = providers.Singleton(
        JudgeService,
        model=judge_model,
    )
