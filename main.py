import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

from config import xpath
from config.hashtags import hashtags
from controllers.tweet_controller import get_tweet_link
from controllers.user_controller import get_account_link
from crawls.tweet_crawler import TweetCrawler

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(3)

# tweet_link = get_tweet_link(driver, hashtags, 5)
# print(json.dumps(tweet_link, indent=4, ensure_ascii=False))

user_link = get_account_link(driver, hashtags, 5)
print(json.dumps(user_link, indent=4, ensure_ascii=False))

driver.quit()

