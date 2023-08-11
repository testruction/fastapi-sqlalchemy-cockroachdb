# -*- coding: utf-8 -*-
import logging
import httpx
from pydantic import BaseModel
from fastapi import Request, APIRouter

from frontendservice.config import args

logger = logging.getLogger(__name__)


class ApiResponseModel(BaseModel):
    status_code: int
    text: str
    data: object


class StatusModel(BaseModel):
    postgres: ApiResponseModel


class StatusApis():
    router = APIRouter()

    @router.get('/status', response_model=StatusModel)
    def status(request: Request):
        # Pass Oauth2 tokens to backend
        access_token = 'n/a' if not request.headers.get('X-Amzn-Oidc-Accesstoken') else request.headers.get('X-Amzn-Oidc-Accesstoken')
        id_token = 'n/a' if not request.headers.get('X-Amzn-Oidc-Data') else request.headers.get('X-Amzn-Oidc-Data')

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json',
                   'X-Amzn-Oidc-Accesstoken': access_token,
                   'X-Amzn-Oidc-Data': id_token}

        with httpx.Client(trust_env=False) as client:
            rsf = client.get(url=f'{args.backend_api_url}/v1/fakenames/postgres?limit=5',
                             headers=headers)
            # logger.info(rsf.text)

            return {
                'postgres': {
                    'status_code': rsf.status_code,
                    'text': rsf.text,
                    'data': rsf.json()
                }
            }
