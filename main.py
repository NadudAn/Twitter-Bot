#-----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-06
#-----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-07
# Content: Chrome Driver Error Correction
#-----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-11
# Content: update url
# -----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-18
# Content: Work on weekdays only
# -----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-21
# Content: Corrected errors
# -----------------------------------
# Project: twitter_project
# Author: Nayeong An
# Date: 2022-09-04
# Content: Revising a code
# -----------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time
import os

API_KEY = 'TWITTER_API_KEY'
API_KEY_SECRET = 'TWITTER_API_SECRET'
ACCESS_TOKEN = 'TWITTER_ACCESS_TOKEN'
ACCESS_TOKEN_SECRET = 'TWITTER_ACCESS_TOKEN_SECRET'

try:
    #key mapping
    api_key = os.environ.get(API_KEY)
    api_secret = os.environ.get(API_KEY_SECRET)
    access_token = os.environ.get(ACCESS_TOKEN)
    access_token_secret = os.environ.get(ACCESS_TOKEN_SECRET)
    
    auth = tweepy.OAuthHandler(consumer_key = api_key, consumer_secret = api_secret)
    auth.set_access_token(access_token, access_token_secret)
except KeyError as e:
    print(e)

day = {
        'Mon' : 0,
        'Tue' : 1,
        'Wed' : 2,
        'Thu' : 3,
        'Fri' : 4,
        'Sat' : 5,
        'Sun' : 6
    }

day_index = str(time.strftime('%a', time.localtime(time.time())));

def tweets():
    try: 
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')               # headless
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
    
        driver = webdriver.Chrome(executable_path="chromedriver", options=chrome_options)
        url = "https://www.kongju.ac.kr/kongju/13157/subview.do"
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        date = str(soup.find('th', class_='on').get_text())
        date = date.replace("  ", " ")

        menus = soup.find_all('td')
        menu = str(menus[day[day_index]].get_text())

        if menu != "등록된 식단내용이(가) 없습니다.": flag = True
        else: flag = False
        
        today = date + "\n\n" + menu

        api = tweepy.API(auth)
        api.update_status(status = today)

    except tweepy.errors.TweepyException as e:
        print(e)

if (day[day_index] < 5) and (flag):
    tweets()