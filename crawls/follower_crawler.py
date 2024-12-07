import json
import time
from selenium.webdriver.common.by import By

from crawls.base_crawler import BaseCrawler

class FollowerCrawler(BaseCrawler):
    def __init__(self, driver, xpath_follower):
        super().__init__(driver)
        self.xpath_follower = xpath_follower

    def get_follower_data(self, element, user_id) :
        follower_data = {}
        try:
            follower_data['user_id'] = user_id
            follower_data['follower_user_id'] = element.find_element(By.XPATH, self.xpath_follower.get('follower_user_id')).text

        except Exception as e:
            print(f"Error extracting data for follower: {str(e)}")
            follower_data = None
        return follower_data

    
    def crawl(self, url):
        followers = []
        
        self.driver.get(url) 
        self.driver.implicitly_wait(10)

        user_id = '@' + self.driver.current_url.split('/')[-2]

        count = 0
        for _ in range(5):
            follower_elements = self.driver.find_elements(By.XPATH, '//button[@data-testid="UserCell"]')
            for follower_element in follower_elements:
                temp = self.get_follower_data(follower_element, user_id)
                if temp not in followers and temp:
                    followers.append(temp)
                    count += 1
            
            # Scroll down using JavaScript
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        print(f'Found {count} followers with user {user_id}')
        # print(json.dumps(followers, indent=4, ensure_ascii=False))
        return followers


