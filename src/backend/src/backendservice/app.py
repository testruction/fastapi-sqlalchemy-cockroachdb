# -*- coding: utf-8 -*-
import uvicorn

from fastapi import FastAPI, Request

from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from backendservice.utils.userid import get_openid_user

# Models (required for initial table creation)
from backendservice.models import postgres
from backendservice.database import engine
# Controlers
from backendservice.controllers.fakenames import FakenamesApis
from backendservice.controllers.status_code import StatusCodeApis
from backendservice.controllers.health import HealthApis


def create_app():
    """
    Web application initialization
    """
    postgres.Base.metadata.create_all(engine)

    app = FastAPI(docs_url="/v1/docs",
                  openapi_url="/v1/openapi.json")

    app.include_router(FakenamesApis.router)
    app.include_router(StatusCodeApis.router)
    app.include_router(HealthApis.router)

    Instrumentator(should_group_status_codes=False,
                   excluded_handlers=[".*admin.*", "/health", "/metrics"],).instrument(app).expose(app)

    # Enable FastApi telemetry
    def request_hook(span: trace.get_current_span(), scope: dict):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user(Request))

    FastAPIInstrumentor().instrument_app(app,
                                         client_request_hook=request_hook,
                                         excluded_urls="/health,/metrics")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=8000)
