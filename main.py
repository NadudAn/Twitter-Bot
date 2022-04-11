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

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import tweepy
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import time

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
    menu = str(menus[day[str(time.strftime('%a', time.localtime(time.time())))]].get_text())

    today = date + "\n\n" + menu

    api = tweepy.API(auth)
    api.update_status(status = today)

except tweepy.errors.TweepyException as e:
    print(e)