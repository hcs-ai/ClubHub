import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

def scrape_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.prettify()
    except requests.RequestException as e:
        print(f"Error scraping {url}: {e}")
        return None

def save_content(content, filename):
    with open("data/" + filename, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    base_url = "https://www.hcsaigroup.org/"
    main_page = scrape_page(base_url)
    
    if main_page:
        save_content(main_page, "main_page.html")
        
        soup = BeautifulSoup(main_page, 'html.parser')
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            
            if full_url.startswith(base_url):
                page_content = scrape_page(full_url)
                if page_content:
                    filename = f"{href.strip('/').replace('/', '_')}.html"
                    save_content(page_content, filename)
                    print(f"Scraped and saved: {full_url}")

if __name__ == "__main__":
    main()