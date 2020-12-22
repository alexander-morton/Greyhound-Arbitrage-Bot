from jewrl import jewrl
from oddscraper import oddscraper
from spreader import spreader

import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver 



if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): #Not sure how this works but it does
    ssl._create_default_https_context = ssl._create_unverified_context


url_dict = jewrl()
for track in url_dict:
    if url_dict[track] != []:
        print("\n")
        odds_dict = oddscraper(url_dict[track][0])
        print(odds_dict)
        
        
