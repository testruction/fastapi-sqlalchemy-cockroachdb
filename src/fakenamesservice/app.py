# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from fakenamesservice.controllers.apis import FakenamesApis
from fakenamesservice.utils.userid import get_openid_user


def create_app():
    """
    API Service initialization
    """
    app = FastAPI()

    app.include_router(FakenamesApis.router)

    # Enable flask telemetry
    def request_hook(span: trace.get_current_span(), scope: dict):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user())
    FastAPIInstrumentor().instrument_app(app,
                                         client_request_hook=request_hook,
                                         excluded_urls="health")

    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), port=8000)
