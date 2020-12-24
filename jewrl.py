
import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver 


def jewrl():
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




    row_heads = page_soup.find_all("p", {"class": "racing-meeting-row__meeting-name"})
    tracks = []
    for track in row_heads:
        tracks.append(track.getText())


    # races = []
    # for row in page_soup.find_all("div", {"class":"racing-meeting-row"}):
    #     track_race=[]
    #     for race in row.find_all("a", {"class": "racing-meeting-cell"}):
    #         track_race.append(race["href"])
    #     races.append(track_race)


    races = []
    for row in page_soup.find_all("div", {"class":"racing-meeting-row"}):
        track_race=[]
        for race in row.find_all("a", {"class": "is-imminent racing-meeting-cell"}):
            track_race.append("https://www.odds.com.au"+race["href"])
        races.append(track_race)

    url_dict = {}

    for track_name in tracks:
        url_dict[track_name] = races.pop(0)

    browser.close()

    return url_dict

