import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_and_parse(url):
    """
    Fetches and parses the webpage content.
    """
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        print("Page fetched successfully!")
    else:
        print(f"Failed to fetch page. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def extract_article_links(soup):
    """
    Extracts the links to the full articles from the main page.
    """
    article_links = []
    cards = soup.find_all('div', attrs={'data-testid': 'edinburgh-card'})
    
    for card in cards:
        link_tag = card.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            # Ensure the link is complete (starts with https://www.bbc.com)
            if not link.startswith('http'):
                link = 'https://www.bbc.com' + link
            article_links.append(link)
    
    return article_links

def format_datetime(iso_date):
    """
    Converts ISO 8601 date to a standard format.
    """
    dt = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def extract_full_article(url):
    """
    Fetches and parses the full article content from the article page.
    """
    soup = fetch_and_parse(url)
    if not soup:
        return None

    # Extract title
    title_tag = soup.find('h1')
    title = title_tag.text.strip() if title_tag else "No title found"

    # Extract full article content
    content = []
    paragraphs = soup.find_all('p')
    for paragraph in paragraphs:
        content.append(paragraph.text.strip())
    
    full_content = " ".join(content)
    
    # Extract main image URL
    img_tag = soup.find('img')
    img_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else "No image found"
    
    # Extract publisher name
    publisher_tag = soup.find('span', class_='sc-b42e7a8f-7')
    if not publisher_tag:
        publisher_tag = soup.find('span', class_='khDNZa')
    publisher = publisher_tag.text.strip() if publisher_tag else "No publisher found"
    
    # Extract publication time and format it
    time_tag = soup.find('time')
    iso_date = time_tag['datetime'] if time_tag else "No publication time found"
    pub_time = format_datetime(iso_date) if iso_date != "No publication time found" else iso_date
    
    return title, full_content, img_url, publisher, pub_time

def main():
    url = "https://www.bbc.com/news"  # Replace with your target URL
    soup = fetch_and_parse(url)
    if soup:
        article_links = extract_article_links(soup)
        
        for i, link in enumerate(article_links, 1):
            title, full_content, img_url, publisher, pub_time = extract_full_article(link)
            if title and full_content:
                print(f"\nArticle {i}:")
                print(f"Title: {title}")
                print(f"Image URL: {img_url}")
                print(f"Publisher: {publisher}")
                print(f"Publication Time: {pub_time}")
                print(f"Content: {full_content[:500]}...")  # Print the first 500 characters for brevity
                print("Read more: " + link)

if __name__ == "__main__":
    main()
