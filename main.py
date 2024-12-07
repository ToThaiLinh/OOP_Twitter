import json
import uuid
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time

from config import xpath
from config.hashtags import hashtags
from controllers.tweet_controller import get_tweet_link
from controllers.user_controller import get_account_link
from crawls.comment_crawler import CommentCrawler
from crawls.follower_crawler import FollowerCrawler
from crawls.following_crawler import FollowingCrawler
from crawls.quote_crawler import QuoteCrawler
from crawls.retweet_crawler import RetweetCrawler
from crawls.tweet_crawler import TweetCrawler
from crawls.user_crawler import UserCrawler
from data.mysql_database import MySQLDatabase
from services.tweet_service import TweetService
from services.user_service import UserService

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

db = MySQLDatabase(host='localhost', user='root', password='', database='twitter')
user_service = UserService(db=db)
tweet_service = TweetService(db = db)

tweet_crawler = TweetCrawler(driver = driver, xpath_tweet= xpath.xpath_tweet)
user_crawler = UserCrawler(driver = driver, xpath_user=xpath.xpath_user)
follower_crawler = FollowerCrawler(driver = driver, xpath_follower= xpath.xpath_follower)
following_crawler = FollowingCrawler(driver = driver, xpath_following=xpath.xpath_following)
comment_crawler = CommentCrawler(driver=driver, xpath_comment=xpath.xpath_comment)
quote_crawler = QuoteCrawler(driver = driver, xpath_quote= xpath.xpath_quote)
retweet_crawler = RetweetCrawler(driver = driver, xpath_retweet=xpath.xpath_retweet)


tweet_links = get_tweet_link(driver, hashtags, 5)
# print(json.dumps(tweet_links, indent=4, ensure_ascii=False))

# users = get_account_link(driver, hashtags, 5)
# print(json.dumps(user_link, indent=4, ensure_ascii=False))

for tweet_link in tweet_links:
    try:
        # Crawl tweet
        tweet_data, user_post, mentions, have_hashtags = tweet_crawler.crawl(tweet_link)

        tweet_id = tweet_data['tweet_id']

        # get tweet_id
        tweet_service.create(**tweet_data)

        try:

            if user_post:
                user_data = user_crawler.crawl(f'https://x.com/{user_post.lstrip("@")}')
                user_service.create(**user_data)

                user_service.save_post_tweet(user_post, tweet_id)
        except Exception as e:
            print('Có lỗi với user_post')

        try:

            users_comment_tweet = comment_crawler.crawl(tweet_link)
            if users_comment_tweet:
                for user_comment_tweet in users_comment_tweet:
                    user_data_comment = user_crawler.crawl(f'https://x.com/{user_comment_tweet["user_id"].lstrip("@")}')
                    user_service.create(**user_data_comment)

                    user_service.save_comment_tweet(**user_comment_tweet)
        except Exception as e:
            print('Có lỗi với user_comment')

        try:
            if have_hashtags:
                for hashtag_name in have_hashtags:
                    tweet_service.save_hashtag(hashtag_name)
                    tweet_service.save_have_hashtag(hashtag_name, tweet_id)
        except Exception as e:
            print('Có lỗi với hava_hashtag')

        try:
            if mentions:
                for user_mention in mentions:
                    user_mention_data = user_crawler.crawl(f'https://x.com/{user_mention.lstrip("@")}')
                    user_service.create(**user_mention_data)

                    user_service.save_mention(user_mention, tweet_id)
        except Exception as e:
            print(f'Có lỗi với mentions')

        try:
            quotes_data = quote_crawler.crawl(tweet_link + '/quotes')
            if quotes_data:
                for quote_data in quotes_data:
                    user_quote_data = user_crawler.crawl(f'https://x.com/{quote_data["user_id"].lstrip("@")}')
                    user_service.create(**user_quote_data)

                    user_service.save_repost(**quote_data)
        except Exception as e:
            print(f'Có lỗi với quote')
        
        try:
            retweets_data = retweet_crawler.crawl(tweet_link + '/retweets')
            if retweets_data:
                for retweet_data in retweets_data:
                    user_retweet_data = user_crawler.crawl(f'https://x.com/{retweet_data["user_id"].lstrip("@")}')
                    user_service.create(**user_retweet_data)

                    user_service.save_repost(**retweet_data)
        except Exception as e:
            print('Có lỗi với retweet')
    except Exception as e:
        print(f'Lỗi xảy ra với {tweet_link}')

# for user in users:
#     user_link = f'https://x.com/{user.lstrip("@")}'

#     user_data = user_crawler.crawl(user_link)
#     user_service.create(**user_data)

#     users_following = following_crawler.crawl(user_link + '/following')
#     if users_following:
#         for user_following in users_following:
#             user_data_following = user_crawler.crawl(f"https://x.com/{user_following['following_user_id'].lstrip('@')}")
#             user_service.create(**user_data_following)
#             user_service.save_following(**user_following)

#     users_follower_common = follower_crawler.crawl(user_link + '/followers')
#     users_follower_verity = follower_crawler.crawl(user_link + '/verified_followers')
#     users_follower_common.extend(users_follower_verity)
#     users_follower = users_follower_common
#     if users_follower:
#         for user_follower in users_follower:
#             user_data_follower = user_crawler.crawl(f"https://x.com/{user_follower['follower_user_id'].lstrip('@')}")
#             user_service.create(**user_data_follower)
#             user_service.save_follower(**user_follower)


user_service.close()
tweet_service.close()

driver.quit()

