# -*- coding: utf-8 -*-
import pytest
import logging
import hashlib
import uuid
import itertools
import pkg_resources
import csv
import json
from datetime import datetime


from contextlib import closing

from fastapi.testclient import TestClient

from backendservice.app import create_app

logger = logging.getLogger(__name__)

dataset = pkg_resources.resource_filename(__name__,
                                          'fakenames.csv')


def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


@pytest.fixture
def client(dbsession) -> TestClient:
    app = create_app()
    client = TestClient(app, raise_server_exceptions=True)
    yield client


def test_route_create(dbsession, client):
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        reader = list(reader)

        payload = reader[35]
        payload['number'] = int(payload['number']) + 100000
        payload['birthday'] = datetime.strptime(payload['birthday'],
                                                '%m/%d/%Y').isoformat()

        # Generate new guid to avoir "existing" error
        payload['guid'] = str(hashlib.sha1(str(uuid.uuid4()).encode('utf-8')).hexdigest()[:35])

        logger.info(f'''
                    action:    "create"
                    number:    "{payload['number']}"
                    firstname: "{payload['givenname']}"
                    lastname:  "{payload['surname']}"
                    guid:      "{payload['guid']}"
                    ''')

        response = client.post("/v1/fakenames/snowflake",
                               content=json.dumps(payload))

    assert response.status_code == 201


def test_route_read_all_limit_default(dbsession, client):
    limit = 100  # Default limit
    response = client.get('/v1/fakenames/snowflake')

    json_data = response.json()
    logger.info(f'Found "{len(json_data)}/{limit}" JSON records')
    assert response.status_code == 200


def test_route_read_all_limit_1000(dbsession, client):
    limit = 1000
    response = client.get(f'/v1/fakenames/snowflake?limit={limit}')

    json_data = response.json()
    logger.info(f'Found "{len(json_data)}/{limit}" JSON records')
    assert response.status_code == 200


def test_route_read(dbsession, client):
    guid = '71160a30-b20f-4cef-91d9-5cf57c5112e4'
    response = client.get(f"/v1/fakenames/snowflake/{guid}")

    json_data = response.json()
    logger.info(f'''
                action:    "read"
                number:    "{json_data['number']}"
                firstname: "{json_data['givenname']}"
                lastname:  "{json_data['surname']}"
                guid:      "{json_data['guid']}"
                ''')
    assert response.status_code == 200


def test_route_patch(dbsession, client):
    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        reader = list(reader)

        payload = reader[30]
        payload['number'] = int(payload['number']) + 30
        payload['birthday'] = datetime.strptime(payload['birthday'],
                                                '%m/%d/%Y').isoformat()

        logger.info(f'''
                    action:    "update"
                    number:    "{payload['number']}"
                    firstname: "{payload['givenname']}"
                    lastname:  "{payload['surname']}"
                    guid:      "{payload['guid']}"
                    ''')

        response = client.patch("/v1/fakenames/snowflake",
                                content=json.dumps(payload))
    assert response.status_code == 200
    assert response.json()['guid'] == payload['guid']
    assert response.json()['number'] == payload['number']


def test_model_delete(dbsession, client):
    guid = '9dc0ed75-61fc-47a4-8ad8-57206ff37add'
    check = client.get(f"/v1/fakenames/snowflake/{guid}")

    json_data = check.json()

    logger.info(f'''
                action:    "delete"
                number:    "{json_data['number']}"
                firstname: "{json_data['givenname']}"
                lastname:  "{json_data['surname']}"
                guid:      "{json_data['guid']}"
                ''')

    response = client.delete(f"/v1/fakenames/snowflake/{json_data['guid']}")
    assert response.status_code == 200
    assert response.json()['deleted'] is True
    assert response.json()['guid'] == json_data['guid']
