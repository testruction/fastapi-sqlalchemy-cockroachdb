import pytest
import logging
from pathlib import Path
import csv
import itertools
from datetime import datetime

from contextlib import closing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backendservice.config import DevelopmentConfig
from backendservice.models import postgres

logger = logging.getLogger(__name__)

dataset = str(Path(__file__).parent / 'unit/fakenames.csv')


@pytest.fixture(scope="session")
def engine():
    return create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI, )


@pytest.fixture(scope="session")
def tables(engine):

    postgres.Base.metadata.create_all(engine)
    yield
    postgres.Base.metadata.drop_all(engine)


@pytest.fixture(scope="session")
def dbsession(engine, tables):
    """ Returns an sqlalchemy session, and after the test tears down everything properly."""
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    Session = sessionmaker(bind=engine)

    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    with Session.begin() as session:
        with closing(open(dataset, encoding='utf-8-sig')) as f:
            reader = csv.DictReader(lower_first(f))

            for row in reader:
                # Parse birthday string to datetime object for SQLAlchemy 2.0 SQLite compatibility
                if 'birthday' in row and row['birthday']:
                    row['birthday'] = datetime.strptime(row['birthday'], '%m/%d/%Y')
                session.add(postgres.Fakenames(**row))
        session.commit()

    yield session

    session.close()
    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()
