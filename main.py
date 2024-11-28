from selenium import webdriver
import time

from crawls.tweet_crawler import TweetCrawler
from crawls.user_crawler import UserCrawler
import config.xpath as xpath

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(5)

user_crawler = UserCrawler(driver= driver, xpath_user = xpath.xpath_user)
tweet_crawler = TweetCrawler(driver = driver, xpath_tweet = xpath.xpath_tweet)

user_crawler.crawl_user("https://x.com/elonmusk")
tweet_crawler.crawl_tweet("https://x.com/Orbler1/status/1861988115717759356")

driver.quit()
