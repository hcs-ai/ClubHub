import requests
from bs4 import BeautifulSoup

# URL of the website you want to scrape
url = "https://hcsaigroup.org/"

# Send a GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find the body tag
body = soup.find('body')

# Check if body
if body:
    # Print the formatted HTML
    with open("data.txt", "w") as file:
        file.write(soup.prettify())