from pydantic import BaseModel

from app.core.domains.judge.model import JudgeMaterial, Keyword


class JudgeRequest(BaseModel):
    """
    Request schema for the judge endpoint.
    """

    topic: str
    judge_materials: list[JudgeMaterial]


class JudgeResponse(BaseModel):
    """
    Response schema for the judge endpoint.
    """

    winner_party_id: str
    verdict: str
    reason: str
    keywords: list[Keyword]
