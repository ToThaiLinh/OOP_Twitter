import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_tweet_link(driver, hashtags, scroll_counts):
    tweets = []
    for hashtag in hashtags[1:2]:

        url = f'https://x.com/hashtag/{hashtag}'
        driver.get(url)
        
        wait = WebDriverWait(driver, 10)

        try:
            wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@lang = "en"]')))
            
            pattern = r"^https://x\.com/[a-zA-Z0-9_]+/status/\d+$"
        
            tweets_text = []
            for _ in range(scroll_counts):
                tweet_elements = driver.find_elements(By.XPATH, '//div[@lang = "en"]')
                for i, tweet in enumerate(tweet_elements):
                    try:
                        tweet_elements = driver.find_elements(By.XPATH, '//div[@lang = "en"]')
                        tweet = tweet_elements[i]

                        if tweet.text not in tweets_text:
                            tweets_text.append(tweet.text)

                            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", tweet)
                            time.sleep(1)

                            tweet.click()
                            time.sleep(2)
                            if re.match(pattern, driver.current_url):
                                tweets.append(driver.current_url)

                            driver.back()
                            time.sleep(2)

                    except Exception as e:
                        print(f"Lỗi khi xử lý phần tử {i + 1}: {e}")

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            print(f'Found {len(tweets)} tweet with {hashtag}.')
        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tìm kiếm hashtag {hashtag}: {e}")

        
    return tweets