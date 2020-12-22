
import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver 

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): #Not sure how this works but it does
    ssl._create_default_https_context = ssl._create_unverified_context

my_url = 'https://www.odds.com.au/greyhounds/'

browser = webdriver.Chrome('/Users/Bet-tings/chromedriver') #The chromedriver filepath required
browser.get(my_url) #This will open a browser with the URL


## REDUNDANT CODE ##
# uclient = urlopen(my_url)
# page_html = uclient.read()
# page_soup = soup(page_html, "html.parser")
# uclient.close()

html = browser.page_source # Use loaded page source on the browser and make html soup 
page_soup = soup(html, "html.parser") 




rows = page_soup.find_all("p", {"class": "racing-meeting-row__meeting-name"})
tracks = []
for track in rows:
    printtrack.getText()