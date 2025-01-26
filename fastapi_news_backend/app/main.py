from fastapi import FastAPI
from app.database import Base, engine
from app.routers import articles, sources,scraping
import uvicorn
from app.routers import summaries

# Create the database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Include routers
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(summaries.router, prefix="/summaries", tags=["Summaries"])
app.include_router(scraping.router, prefix="/scrape-news", tags=["Scraping"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the BBC_News  API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="localhost", port=8011, reload=True)
