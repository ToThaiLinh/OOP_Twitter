import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

from config import hashtags, xpath
from controllers.tweet_controller import get_tweet_link
from crawls.tweet_crawler import TweetCrawler
from crawls.user_crawler import UserCrawler

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

options = Options()
# options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(3)

tweet_crawler = TweetCrawler(driver = driver, xpath_tweet= xpath.xpath_tweet)
tweet_crawler.crawl('https://x.com/elonmusk/status/1865242876625535417')