import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

my_url = 'https://www.odds.com.au/greyhounds/ipswich/race-4/?date=2020-12-22'
uclient = urlopen(my_url)
page_html = uclient.read()
uclient.close()

page_soup = soup(page_html, 'html.parser')

