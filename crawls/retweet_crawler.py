from selenium.webdriver.common.by import By
import time
import json
import uuid

from crawls.base_crawler import BaseCrawler

class RetweetCrawler(BaseCrawler):
    def __init__(self, driver):
        super().__init__(driver)

    def get_retweet_data(self, element_section, i):
        retweet_data = {}
        try:
            retweet_data['respost_id'] = str(uuid.uuid4())
            retweet_data['user_id'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text
            retweet_data['tweet_id'] = self.driver.current_url.split('/')[-2] 
            retweet_data['type'] = 'retweet'
            retweet_data['content'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[2]/span').text
        except Exception as e:
            print(f"Error extracting data for retweet {i}: {str(e)}")
            retweet_data = None
        return retweet_data
    
    def crawl(self, url):
        reposts = []
        self.driver.get(url) 
        self.driver.implicitly_wait(10)
        
        self.scroll_page(scroll_count=3, wait_time=3)
        
        element_section = self.driver.find_element(By.TAG_NAME, 'section') 
        for i in range(1, 10): 
            retweet_data = self.get_retweet_data(element_section, i)
            if retweet_data:
                reposts.append(retweet_data) 
        return reposts
        

