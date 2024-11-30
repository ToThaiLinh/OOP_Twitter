from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

class Crawler:
    def __init__(self, driver):
        self.driver = driver
        self.keyword_container = []

    # Add a keyword to the list
    def add_keyword(self, keyword):
        if keyword not in self.keyword_container:
            self.keyword_container.append(keyword)
            print("Thêm thành công")
        else:
            print("Thêm không thành công. Từ khóa đã tồn tại.")
    
    # Input keywords from the user until "exit" is typed
    def add_keywords_from_input(self):
        print("Nhập từ khóa (nhập 'exit' để dừng):")
        while True:
            keyword = input("Nhập từ khóa: ").strip()
            if keyword.lower() == "exit":
                print("Đã nhập xong")
                break
            self.add_keyword(keyword)

    # Search users by keywords
    def search_users_by_keywords(self):
        accounts = []

        for keyword in self.keyword_container:
            print(f"Đang tìm kiếm người dùng với từ khóa: {keyword}")
            
            # Wait for search input to be visible
            wait = WebDriverWait(self.driver, 20)
            search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='text']")))

            try:
                # Type the keyword and press Enter
                search_input.send_keys(keyword)
                search_input.send_keys(Keys.RETURN)

                # Click on the "People" tab
                people_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text(🙁'People']")))
                people_button.click()
                time.sleep(5)

                index = 0
                # Scroll down 5 times to get user profiles
                for _ in range(5):
                    user_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
                    for user_element in user_elements:
                        temp = user_element.text
                        if temp not in accounts and temp.startswith('@'):
                            accounts.append(temp)
                            index += 1
                    
                    # Scroll down using JavaScript
                    self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                    time.sleep(2)

                print(f"Đã tìm được: {index} users")

            except Exception as e:
                print(f"Đã xảy ra lỗi trong quá trình tìm kiếm: {e}")
            
            # Return to the homepage to continue search
            self.driver.get("https://x.com/home")

        return accounts

    # Search followers of a specific user and return a list of indices from account_list
    def search_follower_by_username(self, username, account_list):
        followers = []

        print(f"Đang tìm kiếm follower của người dùng: {username}")
        
        # Wait for search input to be visible
        wait = WebDriverWait(self.driver, 20)
        search_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='text']")))

        try:
            # Type the username and search for it
            search_input.send_keys(username)

            # Click on the user profile
            user_button = wait.until(EC.visibility_of_element_located((By.XPATH, f"//span[text(🙁'{username}']")))
            user_button.click()
            time.sleep(2)

            # Click on the "Followers" tab
            followers_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text(🙁'Followers']")))
            followers_button.click()
            time.sleep(2)

            # Switch to the Followers tab
            follower_tab_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[text(🙁'Followers']")))
            follower_tab_button.click()
            time.sleep(5)

            index = 0
            # Scroll once to crawl followers
            for _ in range(1):
                user_elements = self.driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
                for user_element in user_elements:
                    temp = user_element.text
                    address = account_list.index(temp) if temp in account_list else -1
                    if temp != username and address != -1 and temp.startswith('@') and address not in followers:
                        followers.append(address)
                        index += 1

                # Scroll down using JavaScript
                self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(2)

            print(f"Đã tìm được: {index} followers")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tìm kiếm: {e}")

        return followers


