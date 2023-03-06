# Pytest SqlAlchemy CockroachDB

Architecture | Instrumentation
------------ | ---------------
![Architecture](./docs/diagrams/architecture.drawio.svg) | ![Instrumentation](./docs/diagrams/instrumentation.drawio.svg)

Initialize the local devlopment environemnt

```bash
hack/init.sh
```

Run the tests

```bash
source .venv/bin/activate
pytest
```

Run the Web application

```bash
hack/make-run.sh
```

Explore the various Web UIs.

* **CockroachDB**: <http://localhost:8080>
* **Jaeger ui**: <http://localhost:16686>
* **Envoy admin**: <http://localhost:8081>
* **FastAPI swagger**: <http://locallhost:8000/docs>
