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


class SummaryFast(BaseModel):
    article_id: int  # correct the key to article_id

    class Config:
        orm_mode = True

class SummaryResponse(BaseModel):
    id: int
    article_id: int  # corrected to article_id
    summary: str  # corrected to summary_text
    created_at: datetime
    class Config:
        orm_mode = True

class SummaryListResponse(BaseModel):
    summaries: List[SummaryResponse]

    class Config:
        orm_mode = True