from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SourceCreate, SourceResponse
from app.crud.sources import create_source, get_sources
from typing import List

router = APIRouter()

@router.post("/", response_model=SourceResponse)
def create_source_endpoint(source: SourceCreate, db: Session = Depends(get_db)):
    return create_source(db, source)

@router.get("/", response_model=List[SourceResponse])
def get_sources_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_sources(db, skip, limit)
