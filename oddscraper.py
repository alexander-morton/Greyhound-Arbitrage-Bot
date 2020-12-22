import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): #Not sure how this works but it does
    ssl._create_default_https_context = ssl._create_unverified_context



my_url = 'https://www.odds.com.au/greyhounds/ipswich/race-4/?date=2020-12-22'
uclient = urlopen(my_url)
page_html = uclient.read()
uclient.close()

page_soup = soup(page_html, 'html.parser')
