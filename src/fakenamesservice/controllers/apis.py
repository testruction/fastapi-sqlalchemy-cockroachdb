# -*- coding: utf-8 -*-
import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fakenamesservice.models import crud, schemas
from fakenamesservice.database import SessionLocal

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

    @router.get('/apis/v1/fakenames', response_model=List[schemas.Fakenames])
    async def get_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        """ Returns all fake identities """
        identities = crud.read_all(db=db, skip=skip, limit=limit)
        return identities

    @router.get('/apis/v1/fakenames/{guid}', response_model=schemas.Fakenames)
    async def get(guid: str, db: Session = Depends(get_db)):
        """ Returns a fake identity based on its GUID """
        identity = crud.read(db, guid=guid)
        if identity is None:
            raise HTTPException(status_code=404, detail="User not found")
        return identity
