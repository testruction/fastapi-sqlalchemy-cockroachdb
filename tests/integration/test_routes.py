# -*- coding: utf-8 -*-
import pytest
import logging

from fastapi.testclient import TestClient

from fakenamesservice.app import create_app

logger = logging.getLogger(__name__)


@pytest.fixture
def client(dbsession) -> TestClient:
    app = create_app()
    client = TestClient(app)
    yield client
    
def test_model_read_all(dbsession, client):
    response = client.get("/apis/v1/fakenames")
    logger.info(response.json())
    assert response.status_code == 200

def test_model_read(dbsession, client):
    guid = '71160a30-b20f-4cef-91d9-5cf57c5112e4'
    response = client.get(f"/apis/v1/fakenames/{guid}")
    logger.info(response.json())
    assert response.status_code == 200