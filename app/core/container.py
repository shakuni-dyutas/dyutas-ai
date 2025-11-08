from dependency_injector import containers, providers
from langchain_groq import ChatGroq

from app.core.domains.judge.judge_service import JudgeService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    judge_model = providers.Singleton(
        ChatGroq,
        model_name=config.groq_model_name,
        api_key=config.groq_api_key,
    )

    judge_service = providers.Singleton(
        JudgeService,
        model=judge_model,
    )
