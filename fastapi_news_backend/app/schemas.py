from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class SourceBase(BaseModel):
    name: str

class SourceCreate(SourceBase):
    pass

class SourceResponse(SourceBase):
    id: int
    class Config:
        orm_mode = True

class ArticleBase(BaseModel):
    title: str
    content: str
    publish_date: Optional[datetime] = None
    source_id: int

class ArticleCreate(ArticleBase):
    pass

class ArticleResponse(ArticleBase):
    id: int
    source: SourceResponse

    class Config:
        orm_mode = True
