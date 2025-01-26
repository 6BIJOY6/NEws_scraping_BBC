from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List

router = APIRouter()

def fetch_and_parse(url):
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        print("Page fetched successfully!")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_article_links(soup):
    article_links = []
    cards = soup.find_all('div', attrs={'data-testid': 'edinburgh-card'})
    
    for card in cards:
        link_tag = card.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            if not link.startswith('http'):
                link = 'https://www.bbc.com' + link
            article_links.append(link)
    
    return article_links

def format_datetime(iso_date):
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_full_article(url):
    soup = fetch_and_parse(url)
    if not soup:
        return None

    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title found"

    content = []
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        content.append(paragraph.text.strip())
    
    full_content = " ".join(content)
    
    img_tag = soup.find('img')
    img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No image found"
    
    publisher_tag = soup.find('span', class_='sc-b42e7a8f-7')
    if not publisher_tag:
        publisher_tag = soup.find('span', class_='khDNZa')
    publisher = publisher_tag.text.strip() if publisher_tag else "No publisher found"
    
    time_tag = soup.find('time')
    iso_date = time_tag['datetime'] if time_tag and 'datetime' in time_tag.attrs else None
    pub_time = format_datetime(iso_date) if iso_date else None
    
    # Print scraped details in the terminal
    print(f"\nTitle: {title}")
    print(f"Content (first 100 chars): {full_content[:100]}")
    print(f"Image URL: {img_url}")
    print(f"Publisher: {publisher}")
    print(f"Publication Time: {pub_time}")
    
    return title, full_content, img_url, publisher, pub_time

@router.post("/scrape-news", response_model=List[schemas.ArticleResponse])
def scrape_news(db: Session = Depends(get_db)):
    url = "https://www.bbc.com/news"
    soup = fetch_and_parse(url)
    if not soup:
        raise HTTPException(status_code=500, detail="Failed to fetch the main news page.")

    article_links = extract_article_links(soup)
    articles = []
    
    for link in article_links:
        article_details = extract_full_article(link)
        if not article_details:
            continue
        title, full_content, img_url, publisher, pub_time = article_details

        source = crud.articles.get_or_create_source(db, publisher)
        article = crud.articles.create_Scraping_article(
            db=db,
            title=title,
            content=full_content,
            publish_date=pub_time,
            source_id=source.id,
        )
        if article:  # Ensure article is valid
            articles.append(article)

    return [article for article in articles if article is not None]  # Filter out None values