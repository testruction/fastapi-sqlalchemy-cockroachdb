# -*- coding: utf-8 -*-
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from backendservice.models import crud

from backendservice.models import schemas
from backendservice.database import SessionLocal

logger = logging.getLogger(__name__)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FakenamesApis():
    router = APIRouter()

    # APIs
    @router.post('/v1/fakenames', response_model=schemas.Fakenames, status_code=201)
    def create(identity: schemas.FakenamesCreate, db: Session = Depends(get_db)):
        """ Create a new fake identity based """
        check = crud.read(db, guid=identity.guid)
        if check:
            raise HTTPException(status_code=400, detail=f'Identity already exists with guid "{check.guid}"')
        return crud.create(db=db, identity=identity)

    @router.get('/v1/fakenames', response_model=List[schemas.Fakenames], status_code=200)
    def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """ Returns all fake identities """
        identities = crud.read_all(db=db, skip=skip, limit=limit)
        return identities

    @router.get('/v1/fakenames/{guid}', response_model=schemas.Fakenames, status_code=200)
    def read(guid: str, db: Session = Depends(get_db)):
        """ Returns a fake identity based on its GUID """
        identity = crud.read(db, guid=guid)
        if identity is None:
            raise HTTPException(status_code=404, detail="User not found")
        return identity

    @router.patch('/v1/fakenames', response_model=schemas.Fakenames, status_code=200)
    def update(identity: schemas.FakenamesUpdate, db: Session = Depends(get_db)):
        """ Returns a fake identity based on its GUID """
        return crud.update(db=db, identity=identity)

    @router.delete('/v1/fakenames/{guid}', response_model=schemas.FakenamesDelete, status_code=200)
    def delete(guid: str, db: Session = Depends(get_db)):
        """ Returns a fake identity based on its GUID """
        return crud.delete(db=db, guid=guid)
