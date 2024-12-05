from selenium.webdriver.common.by import By
from datetime import datetime
import json
from crawls.base_crawler import BaseCrawler
from utils.utils import Converter


class TweetCrawler(BaseCrawler):
    def __init__(self, driver, xpath_tweet):
        super().__init__(driver)
        self.xpath_tweet = xpath_tweet

    def crawl(self, url):

        self.driver.get(url)
        self.driver.implicitly_wait(10)

        try:
            tweet = self.driver.find_element(By.TAG_NAME, 'article')
            tweet_data = {}
            user_post = None
            mentions = []
            hashtags = []

            try:
                user_post = self.driver.find_element(By.XPATH, './div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span').text
            except Exception:
                user_post = None

            try:
                tweet_data['tweet_id'] = self.driver.current_url.split('/')[-1]
            except Exception:
                tweet_data['tweet_id'] = None

            # Extract tweet data
            for key, xpath in self.xpath_tweet.items():
                try:
                    element = tweet.find_element(By.XPATH, xpath)

                    if key == 'content':
                        list_spans = element.find_elements(By.CSS_SELECTOR, 'span')
                        text = "".join([span.text for span in list_spans])
                        tweet_data[key] = text

                        mentions = [word for word in text.split() if word.startswith('@')]
                        hashtags = [word for word in text.split() if word.startswith('#')]

                    elif key == 'media':
                        img_element = element.find_element(By.TAG_NAME, 'img')
                        tweet_data[key] = img_element.get_attribute('src')

                    elif key == 'created_at':
                        raw_text = element.get_attribute('datetime')
                        try:
                            timestamp = datetime.strptime(raw_text, "%Y-%m-%dT%H:%M:%S.%fZ").strftime('%Y-%m-%d %H:%M:%S')
                            tweet_data[key] = timestamp
                        except ValueError:
                            tweet_data[key] = None
                    else:
                        tweet_data[key] = Converter.convert_to_number(element.text)

                except Exception:
                    tweet_data[key] = None  

            print(user_post)
            print(json.dumps(tweet_data, indent=4, ensure_ascii=False))
            print(json.dumps(mentions, indent=4, ensure_ascii=False))
            print(json.dumps(hashtags, indent=4, ensure_ascii=False))
            
            return tweet_data, user_post, mentions, hashtags

        except Exception as e:
            print(f"Error crawling tweet: {e}")
            return None
    

