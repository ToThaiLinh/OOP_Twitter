from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from crawls.base_crawler import BaseCrawler
from crawls.comment_crawler import CommentCrawler
from crawls.follower_crawler import FollowerCrawler
from crawls.following_crawler import FollowingCrawler
from crawls.quote_crawler import QuoteCrawler
from crawls.retweet_crawler import RetweetCrawler
from crawls.tweet_crawler import TweetCrawler
from crawls.user_crawler import UserCrawler
import config.xpath as xpath
from config.hashtags import hashtags
from data.mysql_database import MySQLDatabase
from services.tweet_service import TweetService
from services.user_service import UserService

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(3)



# comment_crawler = CommentCrawler(driver = driver, xpath_comment = xpath.xpath_comment)
# comment_crawler.crawl('https://x.com/SpaceX/status/1862913184015024327')

follower_crawler = FollowerCrawler(driver = driver, xpath_follower=xpath.xpath_follower)
follower_crawler.crawl('https://x.com/cb_doge/followers')

# user_crawler = UserCrawler(driver= driver, xpath_user = xpath.xpath_user)
# # tweet_crawler = TweetCrawler(driver = driver, xpath_tweet = xpath.xpath_tweet)
# db = MySQLDatabase(host='localhost', user='root', password='', database='twitter')
# #tweet_service = TweetService(db = db)
# user_service = UserService(db = db)

# accounts = []


# tweets = []

# url = 'https://x.com/hashtag/blockchain'
# driver.get(url)


# wait = WebDriverWait(driver, 10)
# wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')))

# for _ in range(3):
#     tweet_elements = driver.find_elements(By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')
#     for i, tweet in enumerate(tweet_elements):
#         if tweet not in tweets:
#             try:
#                 tweets.append(tweet)

#                 # Cuộn đến phần tử
#                 actions = ActionChains(driver)
#                 actions.move_to_element_with_offset(tweet, 20, 0).perform()
#                 time.sleep(1)
                
#                 # Click vào phần tử
#                 tweet.text()
#                 tweet.click()
#                 print(f"Đã click vào phần tử {i + 1}: {tweet.text}")
#                 time.sleep(2)
                
#                 # Quay lại trang trước
#                 driver.back()
#                 time.sleep(2)
                
#                 # Cập nhật lại danh sách phần tử
#                 elements = driver.find_elements(By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')
#             except Exception as e:
#                 print(f"Lỗi khi xử lý phần tử {i + 1}: {e}")
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  
# print("Xử lý xong tất cả các phần tử.")
# print(f'Xử lý được {len(tweets)} phần tử')

# url = 'https://x.com/ElonClipsX/status/1862953990566076696/retweets'
# driver.get(url)

# wait = WebDriverWait(driver, 10)
# wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@data-testid="UserCell"]')))

# retweet_crawler = RetweetCrawler(driver = driver, xpath_retweet= xpath.xpath_retweet)
# retweet_crawler.crawl(url)

# quote_crawler = QuoteCrawler(driver = driver, xpath_quote=xpath.xpath_quote)
# quote_crawler.crawl("https://x.com/ElonClipsX/status/1862953990566076696/quotes")




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

# for account in accounts:
#     user = account.lstrip('@')
#     user_data = user_crawler.crawl(f'https://x.com/{user}')
#     user_service.create(**user_data)
#     print('lưu thanh công')
    

# user_crawler.crawl("https://x.com/Locati0ns")
# user_crawler.crawl("https://x.com/maksh07")
# tweet_crawler.crawl("https://x.com/Orbler1/status/1861988115717759356")

# user_service.close()
driver.quit()
