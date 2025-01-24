# scraping/extract.py

from datetime import datetime

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

def extract_full_article(soup):
    """
    Fetches and parses the full article content from the article page.
    """
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
    
    ## Extract publisher name
    publisher_tag = soup.find('span', class_='sc-b42e7a8f-7')
    if not publisher_tag:
        publisher_tag = soup.find('span', class_='khDNZa')
    publisher = publisher_tag.text.strip() if publisher_tag else "No publisher found"
    # Extract publication time and format it
    # time_tag = soup.find('time')
    # iso_date = time_tag['datetime'] if time_tag else "No publication time found"
    # pub_time = format_datetime(iso_date) if iso_date != "No publication time found" else iso_date
    # Extract publication time and format it
    time_tag = soup.find('time')
    if time_tag and 'datetime' in time_tag.attrs:
        iso_date = time_tag['datetime']
        pub_time = format_datetime(iso_date)
    else:
        pub_time = "No publication time found"
    
    return title, full_content, img_url, publisher, pub_time
