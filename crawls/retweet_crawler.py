import json
import time
from selenium.webdriver.common.by import By
import uuid

from crawls.base_crawler import BaseCrawler

class RetweetCrawler(BaseCrawler):
    def __init__(self, driver, xpath_retweet):
        super().__init__(driver)
        self.xpath_retweet = xpath_retweet

    def get_retweet_data(self, element):
        retweet_data = {}
        try:
            retweet_data['user_id'] = element.find_element(By.XPATH, self.xpath_retweet.get('user_id')).text
            retweet_data['tweet_id'] = self.driver.current_url.split('/')[-2] 
            retweet_data['type'] = 'retweet'
            content_elements = element.find_elements(By.XPATH, self.xpath_retweet.get('content'))
            retweet_data['content'] = ' '.join(content.text for content in content_elements).strip()

        except Exception as e:
            print(f"Error extracting data for retweet: {str(e)}")
            retweet_data = None
        return retweet_data
    
    def crawl(self, url):
        retweets = []

        self.driver.get(url) 
        self.driver.implicitly_wait(10)

        count = 0
        for _ in range(2):
            retweet_elements = self.driver.find_elements(By.XPATH, '//button[@data-testid="UserCell"]')
            for retweet_element in retweet_elements:
                temp = self.get_retweet_data(retweet_element)
                if temp not in retweets and temp:
                    retweets.append(temp)
                    count += 1
            
            # Scroll down using JavaScript
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        print(f'Found {count} retweets')
        # print(json.dumps(retweets, indent=4, ensure_ascii=False))
        return retweets
        

