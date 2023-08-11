# -*- coding: utf-8 -*-
import uvicorn
import pkg_resources

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.wsgi import WSGIMiddleware

from prometheus_fastapi_instrumentator import Instrumentator

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace

from frontendservice.config import args
from frontendservice.utils.userid import get_openid_user

# Controllers
from frontendservice.controllers.health import HealthApis
from frontendservice.controllers.status import StatusApis

# Views
from frontendservice.views.index import IndexPage
from frontendservice.views.oauth import OauthPage
from frontendservice.views.postgres import PostgresPage
from frontendservice.views.dashboards.postgres import create_dash_app as create_dash_postgres_app


def create_app():
    """
    Web application initialization
    """
    app = FastAPI()

    STATICS = pkg_resources.resource_filename(__name__,
                                              'static')

    app.mount("/static/", StaticFiles(directory=STATICS), name="static")
    app.include_router(HealthApis.router)
    app.include_router(StatusApis.router)
    app.include_router(IndexPage.router)
    app.include_router(OauthPage.router)
    app.include_router(PostgresPage.router)

    postgres_dash_app = create_dash_postgres_app(requests_pathname_prefix='/postgres/',
                                                 args=args)
    app.mount("/postgres/",
              WSGIMiddleware(postgres_dash_app.server),
              name='postgres')

    Instrumentator().instrument(app).expose(app)
    
    def request_hook(span: trace.get_current_span(), scope: dict):
        if span and span.is_recording():
            span.set_attribute("enduser.id", get_openid_user(Request))

        FastAPIInstrumentor().instrument_app(app,
                                             client_request_hook=request_hook,
                                             excluded_urls="health")
    return app


if __name__ == '__main__':
    uvicorn.run(create_app(), host='0.0.0.0', port=8000)
