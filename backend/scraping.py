import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from openai import OpenAI
from dotenv import load_dotenv
import json

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


def extract_pages(base_url):
    pages = [base_url]
    content = ""
    i = 0 
    while i < len(pages) and i < 10:
        main_page = scrape_page(pages[i])
        if main_page:
            content += main_page
            soup = BeautifulSoup(main_page, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                full_url = urljoin(base_url, href)
                if full_url.startswith(base_url) and full_url not in pages:
                    pages.append(full_url)
        i += 1
    filename = f"{base_url.lstrip('htps').strip(':/').replace('/', '_')}.html"
    save_content(content, filename)
    return content

load_dotenv()
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)
questions = {
    "Club" : "What is the name of the organization?",
    "Description" : "What is a short, two-sentence summary of the organization's purpose, mission, and objective?",
    "Category" : "Categorize this organization into exactly 1 of the following categories: SPORTS, ACADEMIC, PRE-PROFESSIONAL, RELIGIOUS/CULTURAL, COMMUNITY, EXTRACURRICULAR."
}

websites = open("websites.txt", "r", encoding="utf-8").read().splitlines()
data = []
for website in websites:
    content = extract_pages(website)[:100000]
    chat=[
            {
                "role": "system",
                "content": f"Consider the following HTML code for the website of a student organization:\n\n{content}\n\nFor each of the following queries, give an extremely concise answer restricted solely to the scope of the question. Answer only if you can find relevant data in the website that directly contributes to your answer. Otherwise, respond with the string 'N/A'. Do not include any extraneous words, phrases, or characters in your answer beyond your response."
            }
        ]
    club_data = {}
    for i in questions:
        question = questions[i]
        chat.append({
                    "role": "user",
                    "content": question
                })
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages = chat
        )
        chat.append({"role": "assistant", "content": response.choices[0].message.content})
        club_data[i] = response.choices[0].message.content
    club_data["Link"] = website
    data.append(club_data)

json.dump(data, open("data.json", 'w'))