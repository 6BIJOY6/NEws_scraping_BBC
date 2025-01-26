from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Article, Source
from app.schemas import ArticleCreate
from datetime import datetime


def get_or_create_source(db: Session, name: str):
    source = db.query(Source).filter(Source.name == name).first()
    if not source:
        source = Source(name=name)
        db.add(source)
        db.commit()
        db.refresh(source)
    return source
def create_Scraping_article(db: Session, title: str, content: str, publish_date: datetime, source_id: int):
    article = Article(title=title, content=content, publish_date=publish_date, source_id=source_id)
    db.add(article)
    db.commit()
    db.refresh(article)
    return 
def create_article(db: Session, article: ArticleCreate):
    db_source = db.query(Source).filter(Source.id == article.source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="Source not found")
    new_article = Article(**article.dict())
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

def get_articles(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Article).offset(skip).limit(limit).all()

def get_article(db: Session, article_id: int):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

def update_article(db: Session, article_id: int, updated_article: ArticleCreate):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    for key, value in updated_article.dict().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article_id: int):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    db.delete(article)
    db.commit()
    return {"message": "Article deleted successfully"}
