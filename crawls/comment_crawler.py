import json
import time
from selenium.webdriver.common.by import By
import uuid

from crawls.base_crawler import BaseCrawler

class CommentCrawler(BaseCrawler):
    def __init__(self, driver, xpath_comment):
        super().__init__(driver)
        self.xpath_comment = xpath_comment

    def get_comment_data(self, element):
        comment_data = {}
        try:
            comment_data['user_id'] = element.find_element(By.XPATH, self.xpath_comment.get('user_id')).text
            comment_data['tweet_id'] = self.driver.current_url.split('/')[-1] 
        except Exception as e:
            print(f"Error extracting data for comment: {str(e)}")
            comment_data = None
        return comment_data
    
    def crawl(self, url):
        comments = []

        self.driver.get(url) 
        self.driver.implicitly_wait(10)

        user_id_post = self.driver.find_element(By.TAG_NAME, 'article').find_element(By.XPATH, './div/div/div[2]/div[2]/div/div/div[1]/div/div/div[2]/div/div/a/div/span').text

        count = 0
        for _ in range(2):
            comment_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article')
            for comment_element in comment_elements:
                temp = self.get_comment_data(comment_element)
                if temp not in comments and temp and temp != user_id_post:
                    comments.append(temp)
                    count += 1
            
            # Scroll down using JavaScript
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        print(f'Found {count} comments')
        # print(json.dumps(comments, indent=4, ensure_ascii=False))
        return comments
        

