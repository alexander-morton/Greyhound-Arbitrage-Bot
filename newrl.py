import os, ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from selenium import webdriver
import datetime
import time

def newrl():
    my_url = 'https://www.odds.com.au/greyhounds/'

    browser = webdriver.Chrome('/Users/Bet-tings/chromedriver') #The chromedriver filepath required
    browser.get(my_url) #This will open a browser with the URL

    html = browser.page_source # Use loaded page source on the browser and make html soup 
    page_soup = soup(html, "html.parser") 

    race_dct = {}

    row_heads = page_soup.find_all("p", {"class": "racing-meeting-row__meeting-name"})
    tracks = []
    for track in row_heads:
        tracks.append(track.getText())


    row_contents = page_soup.find_all("div",{"class":"racing-meeting-row"})

    i = 0
    while i < len(tracks):
        trackname = tracks[i]
        row = row_contents[i]

        # imminent_races = row.find_all("a", {"class": "is-imminent racing-meeting-cell"})
        races = row.find_all("a", {"class" :"racing-meeting-cell"})

        upcoming = races #+ imminent_races

        race_dct[trackname] = {}


        for race in upcoming:
            race_number = race.find("span", {"class": "racing-meeting-cell__event-number"}).getText()
            race_link = "https://www.odds.com.au" +race["href"]
            race_time = race.find("span", {"class": "racing-meeting-cell__content"}).getText()

            if ":" in race_time :
                race_time_ls = race_time.split(":")
                race_time = datetime.time(int(race_time_ls[0]), int(race_time_ls[1]))

                race_datetime =  datetime.datetime.combine(datetime.date.today(), race_time)
                # now = datetime.datetime.now()
                

                # if race_datetime - now < datetime.timedelta(minutes=25) and race_datetime - now > datetime.timedelta(minutes=0):
                #     race_dct[trackname][race_number] = [race_link,race_time]
                #     print(race_time)

                race_dct[trackname][race_number] = [race_link,race_datetime]
        i += 1
    browser.close()
    return race_dct



def adder(race_dct, ls):

    for track in race_dct:
        if race_dct[track] != {}:

            for race in race_dct[track]:
                race_datetime = race_dct[track][race][1]
                now = datetime.datetime.now()
                
                if race_datetime - now < datetime.timedelta(minutes=15) and race_datetime - now > datetime.timedelta(minutes=0) and (not race_dct[track][race] in ls) :
                    ls.append(race_dct[track][race])
                    

def string_time(string):
    if string == "ENDED":
        return "done"
    time_list = string.split(" ")
    if len(time_list) == 1:
        seconds = int(time_list[0][:-1])
        time_left = datetime.timedelta(seconds=seconds)
        return time_left
    else:
        minutes = int(time_list[0][:-1])
        seconds = int(time_list[1][:-1])
        time_left = datetime.timedelta(minutes=minutes,seconds=seconds)
        return time_left

        
def refresher(ls):
    
    while True:
        i = 0
        while i < len(ls):
            if len(ls[i]) < 3:
                new_browser = webdriver.Chrome('/Users/Bet-tings/chromedriver')
                new_browser.get(ls[i][0])
                ls[i].append(new_browser)
            else:
                ls[i][2].refresh()

            window = ls[i][2].page_source
            window_soup = soup(window, "html.parser")
            time_left = window_soup.find("abbr", {"class":"imminent relative-time__inner"}).find("span").getText()
            time_left = string_time(time_left)
            if time_left == "done" or time_left < datetime.timedelta(seconds = 15):
                ls[i][2].close()
                ls.remove(ls[i])

                print("yeeehaaaa")
                break

            print(time_left)
            time.sleep(4)
            i += 1

ls1 = []
adder(newrl(),ls1)
refresher(ls1)

