from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, utils
from app.database import get_db
from app.crud.articles import get_article
from app.utils.summarizer import generate_summary
from app.crud.summaries import create_summary

router = APIRouter(
)

# Create a Summary for Article
@router.post("/", response_model=schemas.SummaryResponse)
def create_summary(summary: schemas.SummaryFast, db: Session = Depends(get_db)):
    article_id = summary.article_id

    # Fetch the article using the article_id
    article = get_article(db, article_id=article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    article_body = article.content  # 'content' is the field in Article

    # Generate the summary using the summarizer utility
    summary_text = generate_summary(article_body)
    
    # Insert the summary into the database
    db_summary = crud.summaries.create_summary(db=db, summary_text=summary_text, article_id=article_id)

    return db_summary
@router.get("/", response_model=schemas.SummaryListResponse)
def get_all_summaries(db: Session = Depends(get_db)):
    summaries = crud.summaries.get_all_summaries(db)
    return {"summaries": summaries}