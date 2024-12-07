import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def get_account_link(driver, hashtags, scroll_counts):
    accounts = []
    
    for hashtag in hashtags:
        url = f'https://x.com/hashtag/{hashtag}'
        driver.get(url)
            
        wait = WebDriverWait(driver, 10)

        try:
            people_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'People')]")))
            people_button.click()
            time.sleep(5)

            index = 0
            for _ in range(scroll_counts):
                user_elements = driver.find_elements(By.XPATH, "//span[contains(text(), '@')]")
                for user_element in user_elements:
                    temp = user_element.text
                    if temp not in accounts and temp.startswith('@'):
                        accounts.append(temp)
                        index += 1
                
                driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
                time.sleep(2)

            print(f"Founded: {index} users with hashtag {hashtag}")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình tìm kiếm: {e}")

    return accounts