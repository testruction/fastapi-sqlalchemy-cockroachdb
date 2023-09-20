# -*- coding: utf-8 -*-
import logging
import pkg_resources

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

TEMPLATES_DIR = pkg_resources.resource_filename(__name__,
                                                'templates')
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)

logger = logging.getLogger(__name__)


class PostgresPage():
    router = APIRouter()

    # Dashboard
    @router.get('/fakenames', response_class=HTMLResponse, include_in_schema=False, status_code=200)
    def dashboard(request: Request):
        return TEMPLATES.TemplateResponse(name='postgres.html.jinja',
                                          context={'request': request,
                                                   'title': 'frontend service: Postgres',
                                                   'dash_url': '/fakenames/'})
