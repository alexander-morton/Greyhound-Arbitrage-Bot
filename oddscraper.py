import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver 

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): #Not sure how this works but it does
    ssl._create_default_https_context = ssl._create_unverified_context



my_url = 'https://www.odds.com.au/greyhounds/ipswich/race-4/?date=2020-12-22'
browser = webdriver.Chrome('/Users/Bet-tings/chromedriver')
browser.get(my_url)
html = browser.page_source
page_soup = soup(html, 'html.parser')


rows = page_soup.find_all("span", {"class":"octd-left__silk-wrap"})
dogs = {}

for dog in rows:
    dog_name = dog.img["alt"]
    dogs[dog_name] = []


rows = page_soup.find_all("div", {"class":"octd-right__main-row"})

for row in rows:
    odds = row.find_all('div', {"value status class":"octd-right__odds-value-cell"})
    values = []
    for odd in odds:
        dog_odd = odd.getText()
        values.append(dog_odd)
    print(values)
        




