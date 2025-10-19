from fastapi import FastAPI
from app.core.container import Container
from app.core.config import Settings
from app.domains.judge import routers as judge_routers


def create_app() -> FastAPI:
    container = Container()
    container.config.from_pydantic(Settings())

    router_modules = [
        judge_routers,
    ]

    container.wire(modules=router_modules)

    app = FastAPI()
    for module in router_modules:
        app.include_router(module.router, prefix="/api/v1")
    return app


app = create_app()
