# -*- coding: utf-8 -*-
from fastapi import APIRouter


class HealthApis():
    router = APIRouter()

    @router.get('/v1/health', status_code=200)
    def health_page():
        return "OK"
