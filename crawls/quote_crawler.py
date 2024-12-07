import json
import time
from selenium.webdriver.common.by import By
import uuid

from crawls.base_crawler import BaseCrawler

class QuoteCrawler(BaseCrawler):
    def __init__(self, driver, xpath_quote):
        super().__init__(driver)
        self.xpath_quote = xpath_quote

    def get_quote_data(self, element):
        quote_data = {}
        try:
            quote_data['user_id'] = element.find_element(By.XPATH, self.xpath_quote.get('user_id')).text
            quote_data['tweet_id'] = self.driver.current_url.split('/')[-2] 
            quote_data['type'] = 'quote'
            content_elements = element.find_elements(By.XPATH, self.xpath_quote.get('content'))
            quote_data['content'] = ' '.join(content.text for content in content_elements).strip()

        except Exception as e:
            print(f"Error extracting data for quote: {str(e)}")
            quote_data = None
        return quote_data
    
    def crawl(self, url):
        quotes = []

        self.driver.get(url) 
        self.driver.implicitly_wait(10)

        count = 0
        for _ in range(2):
            quote_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article')
            for quote_element in quote_elements:
                temp = self.get_quote_data(quote_element)
                if temp not in quotes and temp:
                    quotes.append(temp)
                    count += 1
            
            # Scroll down using JavaScript
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
            time.sleep(2)
        print(f'Found {count} quotes')
        # print(json.dumps(quotes, indent=4, ensure_ascii=False))
        return quotes
        

