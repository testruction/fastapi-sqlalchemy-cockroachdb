# -*- coding: utf-8 -*-
import logging
import pkg_resources

import jwt

from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

TEMPLATES_DIR = pkg_resources.resource_filename(__name__,
                                                'templates')
TEMPLATES = Jinja2Templates(directory=TEMPLATES_DIR)

logger = logging.getLogger(__name__)


class OauthPage():
    router = APIRouter()

    @router.get('/oauth', response_class=HTMLResponse, include_in_schema=False, status_code=200)
    def oauth(request: Request):
        if not request.headers.get('X-Amzn-Oidc-AccessToken'):
            access_token = 'n/a'
            access_token_decoded = 'n/a'
        else:
            access_token = request.headers.get('X-Amzn-Oidc-AccessToken')
            access_token_decoded = jwt.decode(jwt=access_token,
                                              algorithms=["RS256"],
                                              options={"verify_signature": False})

        if not request.headers.get('X-Amzn-Oidc-Data'):
            id_token = 'n/a'
            id_token_decoded = 'n/a'
        else:
            id_token = request.headers.get('X-Amzn-Oidc-Data')
            id_token_decoded = jwt.decode(jwt=id_token,
                                          algorithms=["RS256"],
                                          options={"verify_signature": False})

        return TEMPLATES.TemplateResponse(name='oauth.html.jinja',
                                          context={'request': request,
                                                   'access_token': access_token,
                                                   'access_token_decoded': access_token_decoded,
                                                   'id_token': id_token,
                                                   'id_token_decoded': id_token_decoded})
