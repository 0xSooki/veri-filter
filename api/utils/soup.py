import requests
import urllib
from bs4 import BeautifulSoup

verified_sources = {
    "www.apnews.com": "div:class:Article",
    "www.bbc.com": "main:id:main-content",
    "www.cnbc.com": "div:class:ArticleBody-articleBody",
}


def get_base_domain(url):
    return urllib.parse.urlparse(url).netloc


def extract_content(url):
    domain = get_base_domain(url)
    if (domain not in verified_sources.keys()):
        return None
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    h1 = soup.find('h1')

    key = verified_sources[domain].split(':')
    content = soup.find(key[0], attrs={key[1]: key[2]})

    if (content is None or h1 is None):
        return None

    return {"TITLE": h1.text, "TEXT": content.text}


def search(text):
    headers = {"Accept-Language": "en-US,en;q=0.9"}
    cookies = {"CONSENT": "YES+cb.20210720-07-p0.en+FX+410"}
    text = urllib.parse.quote_plus(text)
    url = 'https://google.com/search?q=' + text
    request_result = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(request_result.text, "html.parser")
    heading_object = soup.find_all('h3')
    resList = []
    for info in heading_object:
        resList.append(info.getText())
    return resList
