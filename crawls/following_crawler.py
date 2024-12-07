import json
import time
from selenium.webdriver.common.by import By

from crawls.base_crawler import BaseCrawler

class FollowingCrawler(BaseCrawler):
    def __init__(self, driver, xpath_following):
        super().__init__(driver)
        self.xpath_following = xpath_following

    def get_following_data(self, element, user_id) :
        following_data = {}
        try:
            following_data['user_id'] = user_id
            following_data['following_user_id'] = element.find_element(By.XPATH, self.xpath_following.get('following_user_id')).text

        except Exception as e:
            print(f"Error extracting data for following: {str(e)}")
            following_data = None
        return following_data

    
    def crawl(self, url):
        followings = []
        
        self.driver.get(url) 
        self.driver.implicitly_wait(10)

        user_id = '@' + self.driver.current_url.split('/')[-2]

        count = 0
        for _ in range(2):
            following_elements = self.driver.find_elements(By.XPATH, '//button[@data-testid="UserCell"]')
            for following_element in following_elements:
                temp = self.get_following_data(following_element, user_id)
                if temp not in followings and temp:
                    followings.append(temp)
                    count += 1
            
            # Scroll down using JavaScript
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        print(f'Found {count} followings with user {user_id}')
        # print(json.dumps(followings, indent=4, ensure_ascii=False))
        return followings


