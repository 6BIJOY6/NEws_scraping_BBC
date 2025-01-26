from sqlalchemy.orm import Session
from app.models import Summary
from fastapi import HTTPException

def create_summary(db: Session, summary_text: str, article_id: int):
    # Check if a summary already exists for this article_id
    existing_summary = db.query(Summary).filter(Summary.article_id == article_id).first()
    if existing_summary:
        raise HTTPException(status_code=400, detail="Summary for this article already exists")

    # Create a new summary object
    new_summary = Summary(article_id=article_id, summary=summary_text)

    # Add to the database
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    return new_summary
def get_all_summaries(db: Session):
    return db.query(Summary).all()