from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime
from crawls.base_crawler import BaseCrawler
from utils.utils import Converter

class UserCrawler(BaseCrawler):
    def __init__(self, driver, xpath_user):
        super().__init__(driver)
        self.xpath_user = xpath_user
    
    def crawl(self, url):
        user_data = {}  
        try:
            
            self.driver.get(url)
            self.driver.implicitly_wait(10)

            main_element = self.driver.find_element(By.TAG_NAME, "main")

            for key, xpath in self.xpath_user.items():
                try:
                    if key == "role":
                        user_data[key] = self._get_user_role(main_element)
                    elif key in ['following', 'follower']:
                        element = main_element.find_element(By.XPATH, xpath)
                        user_data[key] = Converter.convert_to_number(element.text)
                    elif key == 'posts_cnt':
                        element = main_element.find_element(By.XPATH, xpath)
                        user_data[key] = self._get_posts_count(element)
                    elif key == 'joined_at':
                        element = main_element.find_element(By.XPATH, xpath)
                        user_data[key] = self._get_joined_date(element)
                    else:
                        element = main_element.find_element(By.XPATH, xpath)
                        user_data[key] = element.text
                except Exception as e:
                    print(f"Error while fetching {key}: {str(e)}")
                    user_data[key] = None 

            print(json.dumps(user_data, indent=4, ensure_ascii=False))
            return user_data
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def _get_user_role(self, main_element):
        try:
            role_element = main_element.find_element(By.XPATH, self.xpath_user.get('role'))
            if role_element:
                return 'KOL'
            return 'User'
        except:
            return 'User' 

    def _get_posts_count(self, element):
        try:
            text_cnt = element.text.split()[0]
            return Converter.convert_to_number(text_cnt)
        except Exception as e:
            print(f"Error processing posts count: {str(e)}")
            return None
    
    def _get_joined_date(self, element):
        try:
            words = element.text.split(" ")
            text_time = " ".join(words[-2:])
            return datetime.strptime(text_time, "%B %Y").strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error processing joined date: {str(e)}")
            return None
