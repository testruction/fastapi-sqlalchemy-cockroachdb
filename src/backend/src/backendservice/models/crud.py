import traceback
import logging

from backendservice.config import args

from sqlalchemy.orm import Session

if args.database_engine == "sqlite":
    from backendservice.models import sqlite as models
elif args.database_engine == "cockroachdb":
    from backendservice.models import postgres as models

from backendservice.models import schemas

from fastapi import Request
from backendservice.utils.userid import get_openid_user

from opentelemetry import trace

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


def create(db: Session, identity: schemas.FakenamesCreate):
    """ Creates a database entry """
    response = None

    with tracer.start_as_current_span(name='create') as span:
        span.set_attributes({'enduser.id': get_openid_user(Request)})

        try:
            response = models.Fakenames(**identity.dict())
            guid = identity.guid
            db.add(response)
            db.commit()
            db.refresh(response)

            logger.info(f'Creating row "{guid}" succeeded!')
            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Creating row failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            span.record_exception(e)
            response = False

        span.set_status(status)
    return response


def read_all(db: Session, skip: int = 0, limit: int = 100):
    """ Retreive all records from the table """
    response = None

    with tracer.start_as_current_span(name='read_all') as span:
        span.set_attributes({'enduser.id': get_openid_user(Request)})
        try:
            response = db.query(models.Fakenames).offset(skip).limit(limit).all()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Reading rows failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            span.record_exception(e)

        span.set_status(status)
    return response


def read(db: Session, guid: str):
    """ Retrieves a given identity by its GUID """
    response = None

    with tracer.start_as_current_span(name='read') as span:
        span.set_attributes({'enduser.id': get_openid_user(Request)})
        span.set_attributes({'fakenames.guid': guid})

        try:
            response = db.query(models.Fakenames).filter(models.Fakenames.guid == guid).first()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Reading row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            span.record_exception(e)

        span.set_status(status)
    return response


def update(db: Session, identity: schemas.FakenamesCreate) -> bool:
    """ Update a givent identity """
    response = None
    guid = None

    with tracer.start_as_current_span(name='update') as span:
        span.set_attributes({'enduser.id': get_openid_user(Request)})

        try:
            response = models.Fakenames(**identity.dict())
            guid = response.guid
            db.merge(response)
            db.commit()

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Updating row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            span.record_exception(e)
            response = False

        span.set_status(status)
    return response


def delete(db: Session, guid: str) -> bool:
    """ Deletes a given identity by its GUID """
    response = {'deleted': False,
                'gender': None,
                'nameset': None,
                'title': None,
                'givenname': None,
                'middleinitial': None,
                'surname': None,
                'guid': guid}

    with tracer.start_as_current_span(name='delete') as span:
        span.set_attributes({'enduser.id': get_openid_user(Request)})

        try:
            r = db.query(models.Fakenames).filter(models.Fakenames.guid == guid).first()
            db.query(models.Fakenames).filter(models.Fakenames.guid == guid).delete()
            db.commit()

            response['deleted'] = True
            response['gender'] = r.gender
            response['nameset'] = r.nameset
            response['title'] = r.title
            response['givenname'] = r.givenname
            response['middleinitial'] = r.middleinitial
            response['surname'] = r.surname
            response['guid'] = r.guid

            status = trace.status.Status(trace.StatusCode.OK)
        except Exception:
            e = traceback.format_exc()
            logger.error(f'Deleting row "{guid}" failed!\n{e}')
            status = trace.status.Status(trace.StatusCode.ERROR)
            span.record_exception(e)

        span.set_status(status)
    return schemas.FakenamesDelete(**response)
