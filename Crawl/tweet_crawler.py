from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import json
import Utils.utils as utils


class TweetCrawler:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def crawl_tweet(self):
        """Crawl a specific tweet's data by link and index."""
        self.driver.get(self.url)
        time.sleep(5)

        try:
            tweet = self.driver.find_elements(By.TAG_NAME, 'article')[0]
            tweet_data = {}

            try:
                tweet_data['tweet_id'] = self.driver.current_url.split('/')[-1]
            except Exception:
                tweet_data['tweet_id'] = None

            xpath_tweet = {
                'created_at': './div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time',
                'content': './div/div/div[3]/div[1]/div/div',
                'media': './div/div/div[3]/div[2]/div/div/div/div/div/div/div/a/div/div[2]/div',
                'comment_cnt': './div/div/div[3]/div[5]/div/div/div[1]/button/div/div[2]/span/span/span',
                'repost_cnt': './div/div/div[3]/div[5]/div/div/div[2]/button/div/div[2]/span/span/span',
                'like_cnt': './div/div/div[3]/div[5]/div/div/div[3]/button/div/div[2]/span/span/span',
                'view_cnt': './div/div/div[3]/div[4]/div/div[1]/div/div[3]/span/div/span/span/span'
            }

            # Extract tweet data
            for key, xpath in xpath_tweet.items():
                try:
                    element = tweet.find_element(By.XPATH, xpath)

                    if key == 'content':
                        list_spans = element.find_elements(By.CSS_SELECTOR, 'span')
                        text = "".join([span.text for span in list_spans])
                        tweet_data[key] = text

                        mentions = [word for word in text.split() if word.startswith('@')]
                        hashtags = [word for word in text.split() if word.startswith('#')]

                        tweet_data[f"{key}_mentions"] = mentions
                        tweet_data[f"{key}_hashtags"] = hashtags

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
                        tweet_data[key] = utils.convert_to_number(element.text)

                except Exception:
                    tweet_data[key] = None  # If the element is not found, set to None

            print(json.dumps(tweet_data, indent=4, ensure_ascii=False))
            return tweet_data

        except Exception as e:
            print(f"Error crawling tweet: {e}")
            return None
