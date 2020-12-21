
import os, ssl

from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context


my_url = 'https://www.odds.com.au/greyhounds/'

uclient = urlopen(my_url)
page_html = uclient.read()
uclient.close()

page_soup = soup(page_html, "html.parser")
print(page_soup.body.div)
tracks = page_soup.findAll("div",{"class":"racing-meeting-row__header"})
print(len(tracks))

