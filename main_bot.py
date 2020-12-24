import os, ssl
import schedule
import time

from jewrl import jewrl
from oddscraper import oddscraper
from spreader import spreader
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver 



if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): #Not sure how this works but it does
    ssl._create_default_https_context = ssl._create_unverified_context

def check():
    url_dict = jewrl()
    for track in url_dict:
        if url_dict[track] != []:
            
            
            odds_dict = oddscraper(url_dict[track][0])
            if not spreader(odds_dict)[0]:
                f = open("success.txt", "a")
                f.write(str(spreader(odds_dict)[0]) + str(spreader(odds_dict)[1]) + track +"\n")
                f.close()




while True:
    check()
    time.sleep(60)

        
