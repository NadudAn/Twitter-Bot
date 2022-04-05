# Project: twitter_project
# Author: Nayeong An
# Date: 2022-04-06

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



driver = webdriver.Chrome(executable_path="chromedriver")
url = "https://www.kongju.ac.kr/kongju/13157/subview.do?enc=Zm5jdDF8QEB8JTJGZGlldCUyRmtvbmdqdSUyRjYlMkZ2aWV3LmRvJTNGbW9uZGF5JTNEMjAyMi4wMy4yOCUyNndlZWslM0RuZXh0JTI2"
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'html.parser')

day = {
    'Mon' : 0,
    'Tue' : 1,
    'Wed' : 2,
    'Thu' : 3,
    'Fri' : 4,
    'Sat' : 5,
    'Sun' : 6
}

date = str(soup.find('th', class_='on').get_text())
date = date.replace("  ", " ")

menus = soup.find_all('td')
menu = str(menus[day[str(time.strftime('%a', time.localtime(time.time())))]].get_text())

today = date + "\n\n" + menu

api = tweepy.API(auth)
api.update_status(status = today)
