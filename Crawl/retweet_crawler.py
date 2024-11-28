from selenium.webdriver.common.by import By
import time
import json
import uuid

class RetweetCrawler:
    def __init__(self, driver, url):
        self.driver = driver
        self.url = url
        self.reposts = []
    
    def scroll_page(self, scroll_count=3, wait_time=3):
        """Cuộn trang để tải thêm nội dung."""
        for _ in range(scroll_count):
            self.driver.execute_script("window.scrollTo(0, 500)")  # Cuộn trang xuống
            time.sleep(wait_time)  # Đợi một chút để trang tải thêm nội dung

    def get_retweet_data(self, i, element_section):
        """Thu thập dữ liệu của một retweet."""
        retweet_data = {}
        try:
            retweet_data['respost_id'] = str(uuid.uuid4())  # Tạo id ngẫu nhiên cho repost
            retweet_data['user_id'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text
            retweet_data['id'] = self.driver.current_url.split('/')[-2]  # Lấy id của bài viết
            retweet_data['type'] = 'retweet'
            retweet_data['content'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[2]/span').text
        except Exception as e:
            print(f"Error extracting data for retweet {i}: {str(e)}")
            retweet_data = None
        return retweet_data
    
    def crawl_retweets(self):
        """Thu thập thông tin retweets từ trang."""
        self.driver.get(self.url)  # Truy cập URL cần thu thập
        time.sleep(5)
        
        # Cuộn trang để tải thêm retweets
        self.scroll_page(scroll_count=3, wait_time=3)
        
        element_section = self.driver.find_element(By.TAG_NAME, 'section')  # Lấy phần tử chứa retweets
        for i in range(1, 10):  # Lặp qua các retweets (ở đây lấy 9 retweets)
            retweet_data = self.get_retweet_data(i, element_section)
            if retweet_data:
                self.reposts.append(retweet_data)  # Thêm vào danh sách repost
        
    def run(self):
        """Chạy toàn bộ quá trình thu thập."""
        self.crawl_retweets()
        # Trả về kết quả dưới dạng JSON
        return json.dumps(self.reposts, indent=4, ensure_ascii=False)

