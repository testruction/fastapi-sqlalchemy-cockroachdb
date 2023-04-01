# -*- coding: utf-8 -*-
import logging
import pkg_resources

from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = pkg_resources.resource_filename(__name__,
                                                'templates')
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)

logger = logging.getLogger(__name__)


class IndexPage():
    router = APIRouter()

    @router.get('/', response_class=HTMLResponse, include_in_schema=False, status_code=200)
    def index(request: Request):
        logger.info(f'Generating "/" route from "{TEMPLATES}/index.html.jinja')

        return TEMPLATES.TemplateResponse(name='index.html.jinja',
                                          context={'request': request,
                                                   'title': 'frontend service'})

    @router.get('/health', include_in_schema=False, status_code=200)
    def health_page():
        return "OK"
