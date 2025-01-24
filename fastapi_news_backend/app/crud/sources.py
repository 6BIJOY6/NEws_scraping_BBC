from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Source
from app.schemas import SourceCreate

def create_source(db: Session, source: SourceCreate):
    db_source = db.query(Source).filter(Source.name == source.name).first()
    if db_source:
        raise HTTPException(status_code=400, detail="Source already exists")
    new_source = Source(name=source.name)
    db.add(new_source)
    db.commit()
    db.refresh(new_source)
    return new_source

def get_sources(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Source).offset(skip).limit(limit).all()
