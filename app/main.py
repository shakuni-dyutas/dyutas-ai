from fastapi import FastAPI

from app.core.container import Container
from app.router import judge


def create_app() -> FastAPI:
    container = Container()

    router_modules = [
        judge,
    ]

    container.wire(modules=router_modules)

    app = FastAPI()
    for module in router_modules:
        app.include_router(module.router, prefix="/api/v1")
    return app


app = create_app()
