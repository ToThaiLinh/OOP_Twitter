import json
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from data.mysql_database import MySQLDatabase
import os
from dotenv import load_dotenv

from config import xpath
from config.hashtags import hashtags
from controllers.tweet_controller import get_tweet_link
from controllers.user_controller import get_account_link
from crawls.tweet_crawler import TweetCrawler
from services.user_service import UserService
# Load environment variables
load_dotenv()

# Database configuration
db_config = {
    'host': os.getenv('HOST'),
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'database': os.getenv('DATABASE')
}

# Initialize database connection
db = MySQLDatabase(**db_config)
user_service = UserService(db)

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

user_links = get_account_link(driver, hashtags, 5)
print(json.dumps(user_links, indent=4, ensure_ascii=False))

# Debugging: Print the type of user_links and its elements
print(f"user_links type: {type(user_links)}")
if isinstance(user_links, list):
    for i, user_link in enumerate(user_links):
        print(f"user_link[{i}] type: {type(user_link)}")

# Save user_links to database
try:
    for user_link in user_links:
        user_service.create(user_link['user_id'], user_link['username'], user_link['role'], user_link['joined_at'], user_link['following'], user_link['follower'], user_link['posts_cnt'])
finally:
    user_service.close()

driver.quit()
