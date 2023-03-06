# -*- coding: utf-8 -*-
import pytest
import logging
import json
import itertools
import pkg_resources
import csv

from contextlib import closing

from fastapi.testclient import TestClient

from fakenamesservice.app import create_app

logger = logging.getLogger(__name__)

dataset = pkg_resources.resource_filename(__name__,
                                          'fakenames.csv')

def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


@pytest.fixture
def client(dbsession) -> TestClient:
    app = create_app()
    client = TestClient(app)
    yield client


def test_route_post(dbsession, client):
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        reader = list(reader)

        payload = reader[35]
        payload['number'] = int(payload['number']) + 9000

        json_data = json.dumps(payload)

        response = client.post("/apis/v1/fakenames/",
                               json=json_data)
    assert response.status_code == 200


def test_route_get_all_limit_default(dbsession, client):
    limit = 100  # Default limit
    response = client.get('/apis/v1/fakenames')

    json_data = response.json()
    logger.info(f'Found "{len(json_data)}/{limit}" JSON records')
    assert response.status_code == 200


def test_route_read_all_limit_1000(dbsession, client):
    limit = 1000
    response = client.get(f'/apis/v1/fakenames?limit={limit}')
    
    json_data = response.json()
    logger.info(f'Found "{len(json_data)}/{limit}" JSON records')
    assert response.status_code == 200


def test_route_read(dbsession, client):
    guid = '71160a30-b20f-4cef-91d9-5cf57c5112e4'
    response = client.get(f"/apis/v1/fakenames/{guid}")
    
    json_data = response.json()
    logger.info(f'''
                action:    "read"
                number:    "{json_data['number']}"
                firstname: "{json_data['givenname']}"
                lastname:  "{json_data['surname']}"
                guid:      "{json_data['guid']}"
                ''')
    assert response.status_code == 200
