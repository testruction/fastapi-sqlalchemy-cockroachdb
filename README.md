# FastAPI SqlAlchemy CockroachDB

This project aims to demonstrate the implementation of the following architectural patterns in Python.

* Model-View-Controller (MVC)
* Frontend/Backend segregation
* 15Factor
* Test-Driven Development

## Architecture

The project is based on two main services:

* **frontendservice**: Frontend mixing ASGI (FastAPI) and WSGI (Flask/Dash) applications.
* **backendservice**: Restful API connected to a database running in a PostgreSQL compatible CockroachDB cluster.


| Architecture | Instrumentation
| :--: | :--: |
| ![](./docs/diagrams/architecture.drawio.svg) | ![](./docs/diagrams/instrumentation.drawio.svg)


[Docker Desktop](https://www.docker.com/products/docker-desktop/) est également requis.

### Initialization

Install [Micromamba](https://mamba.readthedocs.io/en/latest/installation.html#micromamba)
Copy the [.env.example](./.env.example) file and name it `.env`.
Update the variables inside the `.env` file, the run the following command line to create the Python environment dedicated to the project.

```bash
source .env
micromamba create --name ${PROJECT_NAME} --channel conda-forge python=3.10 --yes
```

Activate the environment.

```bash
source .env
micromamba activate ${PROJECT_NAME}
```

### Agencement de l'arborescence de répertoires

```
|-- deploy
|   |-- envoy               # Envoy Proxy manifests
|-- docs                    # Documentation
|-- make                    # local execution scripts
|-- specs                   # Open API definitions
|-- src
|   |-- backend             # "backendservice" source code
|   |-- frontend            # "frontendservice" source code
|-- tests
|   |-- unit                # Unit tests
|   |-- integration         # Integration tests
|-- .env                    # Local variables required for local development
|-- docker-compose.yml      # Local execution environment
|-- pytest.ini              # PyTest configuration
|-- VERSION                 # Application version
```

### Exécution des scripts

The [make](./make/) contains scripts to managed the application lifecyle from the developer workstation.

* [make/init.sh](./make/init.sh) Initialze the development environment (i.e. Environment variable, Python environment, etc.)
* [make/run.sh](./make/run.sh) Build and locally executes the containerized using Docker Compose

## Tests

### Local

Two type of tests can be executed:

* [src/backend/src/tests/unit](./src/backend/src/tests/unit): Unitest written using Pytest to validated the models and controllers
* [tests/integration](./tests/integration): Test written using Thundclient (Postman equivalent for VsCode)

Run the following command to start the Docker Compose environment.

```bash
make/run.sh
```

From a second terminal session, run the following command to start and interactive session in the `backend` container.

```bash
docker compose exec -it --user 'root' backend /bin/bash
```

Run the following commands to run the unit tests.

```bash
# Modèles uniquement
pytest tests/unit/test_models.py

# Routes/Contrôlleurs uniquement
pytest tests/unit/test_route.py

# Tous les tests unitaires
pytest
```

## Running the demo

Don't forget to initialize the environment variables (i.e. `source .env`)

Unit tests are using a SqlAlchemy fixed that load/unload the data in the database

Run the following command to populate

```bash
make/run.sh
```

```bash
docker compose exec -it --user 'root' backend /bin/bash
```

```bash
python3 tests/populate.py
```
