# scraping/fetch.py

import requests
from bs4 import BeautifulSoup

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
