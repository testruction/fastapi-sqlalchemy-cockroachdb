import os
import random

from locust import (HttpUser,
                    FastHttpUser,
                    task,
                    tag)


class Backend(HttpUser):
    @tag("health")
    @task
    def test_health(self):
        self.client.get(url='/health')

    @tag("monitoring")
    @task
    def test_metrics(self):
        self.client.get(url='/metrics')


class BackendApis(FastHttpUser):
    @tag("read")
    @task
    def test_default(self):
        self.rest(method='GET', url='/v1/fakenames/postgres')

    @tag("read")
    @task
    def test_limit5(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=5')

    @tag("read")
    @task
    def test_limit10(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=10')

    @task
    def test_limit25(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=25')

    @tag("read")
    @task
    def test_limit50(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=50')

    @tag("read")
    @task
    def test_limit100(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=100')

    @tag("read")
    @task
    def test_limit1000(self):
        self.rest(method='GET', url='/v1/fakenames/postgres?limit=1000')

    @tag("read")
    @task
    def test_guid(self):
        skip = random.randrange(start=0, stop=1000)
        with self.rest(method='GET', url=f'/v1/fakenames/postgres?skip={skip}&limit=1') as response:
            guid = response.js[0]['guid']
            self.client.get(url=f'/v1/fakenames/postgres/{guid}')