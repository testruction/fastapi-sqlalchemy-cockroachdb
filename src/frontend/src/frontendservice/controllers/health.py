# -*- coding: utf-8 -*-
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)


class HealthApis():
    router = APIRouter()

    @router.get('/health')
    def health_page():
        return "OK"
