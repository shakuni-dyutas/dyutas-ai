from typing import Annotated
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide

from app.core.container import Container
from app.schema.judge import JudgeRequest, JudgeResponse
from app.core.domains.judge.judge_service import JudgeService

router = APIRouter()


@router.post("/judge")
@inject
async def judge(
    request: JudgeRequest,
    service: Annotated[JudgeService, Depends(Provide[Container.judge_service])],
) -> JudgeResponse:
    verdict = await service.judge(request.topic, request.judge_materials)
    return JudgeResponse(**verdict.model_dump())
