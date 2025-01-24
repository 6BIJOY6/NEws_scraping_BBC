from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ArticleCreate, ArticleResponse
from app.crud.articles import (
    create_article, get_articles, get_article, update_article, delete_article
)
from typing import List

router = APIRouter()

@router.post("/", response_model=ArticleResponse)
def create_article_endpoint(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)

@router.get("/", response_model=List[ArticleResponse])
def get_articles_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_articles(db, skip, limit)

@router.get("/{article_id}", response_model=ArticleResponse)
def get_article_endpoint(article_id: int, db: Session = Depends(get_db)):
    return get_article(db, article_id)

@router.put("/{article_id}", response_model=ArticleResponse)
def update_article_endpoint(article_id: int, updated_article: ArticleCreate, db: Session = Depends(get_db)):
    return update_article(db, article_id, updated_article)

@router.delete("/{article_id}")
def delete_article_endpoint(article_id: int, db: Session = Depends(get_db)):
    return delete_article(db, article_id)
