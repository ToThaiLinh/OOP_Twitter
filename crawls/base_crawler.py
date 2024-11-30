import time

class BaseCrawler:
    def __init__(self, driver):
        self.driver = driver

    def load_page(self, url, wait_time=10):
        self.driver.get(url)
        self.driver.implicitly_wait(wait_time)

    def scroll_page(self, scroll_count=3, wait_time=3):
        for _ in range(scroll_count):
            print("Scrolling the page...")
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(wait_time)

    def find_element_safe(self, parent, by, value):
        try:
            return parent.find_element(by, value)
        except Exception as e:
            print(f"Error finding element ({value}): {str(e)}")
            return None
