from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)

driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(3)

tweets = []

url = 'https://x.com/hashtag/blockchain'
driver.get(url)

# Chờ trang tải xong
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')))

# Cuộn và xử lý tweet
for _ in range(3):  # Thử cuộn trang 3 lần
    tweet_elements = driver.find_elements(By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')
    for i, tweet in enumerate(tweet_elements):
        try:
            # Cập nhật lại danh sách `tweet_elements` để tránh phần tử cũ bị lỗi
            tweet_elements = driver.find_elements(By.XPATH, '//div[@lang="en" and @data-testid="tweetText"]')
            tweet = tweet_elements[i]

            # Kiểm tra xem tweet đã được xử lý chưa
            if tweet.text not in tweets:
                tweets.append(tweet.text)

                # Cuộn đến phần tử
                driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", tweet)
                time.sleep(1)

                # Click vào phần tử
                tweet.click()
                print(f"Đã click vào phần tử {i + 1}: {driver.current_url}")
                time.sleep(2)

                # Quay lại trang trước
                driver.back()
                time.sleep(2)

        except Exception as e:
            print(f"Lỗi khi xử lý phần tử {i + 1}: {e}")

    # Cuộn xuống cuối trang để tải thêm phần tử
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

print(f'Xử lý được {len(tweets)} phần tử.')


driver.quit()

