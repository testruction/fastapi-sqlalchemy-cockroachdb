#!/usr/bin/env python3
import datetime
import logging
import pkg_resources
import itertools
import csv
from contextlib import closing

from backendservice.database import SessionLocal, engine

from backendservice.config import args

if args.database_engine == "sqlite":
    from backendservice.models import sqlite as models
elif args.database_engine == "cockroachdb":
    from backendservice.models import postgres as models

logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logger.setLevel('INFO')

dataset = pkg_resources.resource_filename(__name__,
                                          '../tests/unit/fakenames.csv')


def lower_first(iterator):
    return itertools.chain([next(iterator).lower()], iterator)


with SessionLocal() as session:
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)

    with closing(open(dataset, encoding='utf-8-sig')) as f:
        reader = csv.DictReader(lower_first(f))
        for row in reader:
            if args.database_engine == "sqlite":
                day = int(row['birthday'].split('/')[1])
                month = int(row['birthday'].split('/')[0])
                year = int(row['birthday'].split('/')[2])
                row['birthday'] = datetime.date(year, month, day)

            data = models.Fakenames(**row)

            session.add(data)
    session.commit()
