from selenium.webdriver.common.by import By
import json
from datetime import datetime

class UserCrawler:
    def __init__(self, driver, url, xpath_user, converter):
        self.driver = driver
        self.url = url
        self.xpath_user = xpath_user
        self.converter = converter
    
    def crawl(self):
        user_data = {}  # Khởi tạo user_data ngoài vòng lặp
        try:
            # Truy cập link
            self.driver.get(self.url)
            self.driver.implicitly_wait(10)

            # Lấy phần tử chính
            main_element = self.driver.find_element(By.TAG_NAME, "main")

            # Lặp qua các key trong xpath_user để thu thập dữ liệu
            for key, xpath in self.xpath_user.items():
                try:
                    element = main_element.find_element(By.XPATH, xpath)

                    if key == "role":
                        # Kiểm tra vai trò người dùng
                        user_data[key] = self._get_user_role(main_element)
                    elif key in ['following', 'follower']:
                        user_data[key] = self.converter.convert_to_number(element.text)
                    elif key == 'posts_cnt':
                        user_data[key] = self._get_posts_count(element)
                    elif key == 'joined_at':
                        user_data[key] = self._get_joined_date(element)
                    else:
                        # Các giá trị khác
                        user_data[key] = element.text
                except Exception as e:
                    print(f"Error while fetching {key}: {str(e)}")
                    user_data[key] = None  # Lỗi thì gán None

            # In dữ liệu thu thập được
            print(json.dumps(user_data, indent=4, ensure_ascii=False))
            return user_data
        
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def _get_user_role(self, main_element):
        """Lấy vai trò người dùng, nếu là KOL thì trả về 'KOL', nếu không thì là 'User'"""
        try:
            role_element = main_element.find_element(By.XPATH, self.xpath_user.get('role'))
            return 'KOL'  # Nếu tìm thấy vai trò
        except:
            return 'User'  # Nếu không tìm thấy vai trò, mặc định là 'User'

    def _get_posts_count(self, element):
        """Lấy số bài đăng"""
        try:
            text_cnt = element.text.split()[0]
            return self.converter.convert_to_number(text_cnt)
        except Exception as e:
            print(f"Error processing posts count: {str(e)}")
            return None
    
    def _get_joined_date(self, element):
        """Chuyển đổi thời gian tham gia"""
        try:
            words = element.text.split(" ")
            text_time = " ".join(words[-2:])
            return datetime.strptime(text_time, "%B %Y").strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error processing joined date: {str(e)}")
            return None
