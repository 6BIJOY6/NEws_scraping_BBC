from fetch import fetch_and_parse
from extract import extract_article_links, extract_full_article
from db_operation import insert_source, insert_article, insert_image
from datetime import datetime

def main():
    url = "https://www.bbc.com/news"
    soup = fetch_and_parse(url)
    if soup:
        article_links = extract_article_links(soup)
        
        for i, link in enumerate(article_links, 1):
            article_soup = fetch_and_parse(link)
            if article_soup:
                title, full_content, img_url, publisher, pub_time = extract_full_article(article_soup)
                
                # Handle invalid publication time
                if pub_time == "No publication time found":
                    pub_time = None  # Use None for missing publication times
                else:
                    try:
                        # Try parsing the publication time into a datetime object
                        pub_time = datetime.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        print(f"Invalid publication time format for article: {pub_time}")
                        pub_time = None
                
                print(f"\nArticle {i}:")
                print(f"Title: {title}")
                print(f"Image URL: {img_url}")
                print(f"Publisher: {publisher}")
                print(f"Publication Time: {pub_time}")
                print(f"Content: {full_content[:500]}...")
                print("Read more: " + link)
                
                # Insert source and get source_id dynamically
                source_id = insert_source(publisher)
                
                # Insert article into the database using the fetched source_id
                article_id = insert_article(title, full_content, pub_time, source_id)
                
                # Insert image URL into the database using the fetched article_id
                insert_image(article_id, img_url)

if __name__ == "__main__":
    main()
