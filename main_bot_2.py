import schedule
import time
from newrl import  newrl, adder, string_time, refresher, oddscraper2 
import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver

ls = []
race_dct = {}

def update_race_dct():
    global race_dct 
    race_dct = newrl()
    
def update_ls():
    global ls
    global race_dct
    adder(race_dct,ls)


update_race_dct()
update_ls()


schedule.every(30).minutes.do(update_race_dct)
schedule.every(5).minutes.do(update_ls)


while True:
    schedule.run_pending()
    refresher(ls)
    time.sleep(1)
    print("cycled\n")
    
    
    