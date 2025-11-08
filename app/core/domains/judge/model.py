from typing import Annotated
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    text: list[str] | None = None
    image_urls: list[str] | None = None


class JudgeMaterial(BaseModel):
    party_id: str
    argument: str
    evidence: Evidence | None = None


class Verdict(BaseModel):
    """
    Verdict schema for the judge result.
    Winner party id must be inside of the judge materials party_id.
    """

    winner_party_id: Annotated[str, Field(description="The party that won the trial")]
    verdict: Annotated[str, Field(description="The verdict of the trial")]
    reason: Annotated[str, Field(description="The reasoning behind the verdict")]
