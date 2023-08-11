# -*- coding: utf-8 -*-
import uvicorn

from fastapi import FastAPI, Request

from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from backendservice.utils.userid import get_openid_user


# Controlers
from backendservice.controllers.postgres import FakenamesApis as PostgresApis
from backendservice.controllers.health import HealthApis


def create_app():
    """
    Web application initialization
    """
    app = FastAPI(docs_url="/v1/docs",
                  openapi_url="/v1/openapi.json")

    app.include_router(PostgresApis.router)
    app.include_router(HealthApis.router)

    Instrumentator().instrument(app).expose(app)

    # Enable FastApi telemetry
    def request_hook(span: trace.get_current_span(), scope: dict):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user(Request))

    FastAPIInstrumentor().instrument_app(app,
                                         client_request_hook=request_hook,
                                         excluded_urls="health")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=8000)
