from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)

    # Relationship to the articles table
    articles = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    publish_date = Column(DateTime, default=datetime.utcnow)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)

    # Relationship to the source table
    source = relationship("Source", back_populates="articles")
