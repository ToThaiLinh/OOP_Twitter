from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from crawls.base_crawler import BaseCrawler
from crawls.tweet_crawler import TweetCrawler
from crawls.user_crawler import UserCrawler
import config.xpath as xpath
from config.hashtags import hashtags

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(3)

user_crawler = UserCrawler(driver= driver, xpath_user = xpath.xpath_user)
# tweet_crawler = TweetCrawler(driver = driver, xpath_tweet = xpath.xpath_tweet)

accounts = []

# for hashtag in hashtags[0:1]:
#     url = f'https://x.com/hashtag/{hashtag}'
#     driver.get(url)

#     wait = WebDriverWait(driver, 10)
#     people_button = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a')))
#     people_button.click()
#     time.sleep(5)

#     index = 0
#     # Scroll down 5 times to get user profiles
#     for _ in range(2):
#         user_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
#         for user_element in user_elements:
#             temp = user_element.text
#             if temp not in accounts and temp.startswith('@'):
#                 accounts.append(temp)
#                 print(temp)
#                 index += 1
        
#         # Scroll down using JavaScript
#         driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
#         time.sleep(2)

#     print(f"Đã tìm được: {index} users")

# for account in accounts[0:10]:
#     user = account.lstrip('@')
#     user_crawler.crawl(f'https://x.com/{user}')
    

user_crawler.crawl("https://x.com/Locati0ns")
user_crawler.crawl("https://x.com/maksh07")
# tweet_crawler.crawl("https://x.com/Orbler1/status/1861988115717759356")

driver.quit()
