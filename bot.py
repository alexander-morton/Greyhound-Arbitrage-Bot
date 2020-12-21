
import os, ssl

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


my_url = 'https://www.odds.com.au/greyhounds/'

uclient = urlopen(my_url)
page_html = uclient.read()
page_soup = soup(page_html, "html.parser")
uclient.close()



rows = page_soup.find_all("a", {"class": "event-lists__link"})
print(len(rows))
print(rows)
