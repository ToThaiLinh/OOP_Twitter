xpath_tweet = {
    #'tweet_id': '',
    'create_at' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time',
    'content' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[1]/div/div',
    'media' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[2]/div/div/div/div/div/div/div/a/div/div[2]/div',
    'comment_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[1]/button/div/div[2]/span/span/span',
    'repost_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[2]/button/div/div[2]/span/span/span',
    'like_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[3]/button/div/div[2]/span/span/span',
    'view_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[3]/span/div/span/span/span'
}

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime
import utils

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })
time.sleep(5)

driver.get("https://x.com/elonmusk/status/1859472839792820276")
time.sleep(5)

try:
    tweet = driver.find_element(By.TAG_NAME, 'main')
    tweet_data = {}
    try:
        tweet_data['tweet_id'] = driver.current_url.split('/')[-1]
    except Exception as e:
        tweet_data['tweet_id'] = None
    # Tìm và trích xuất dữ liệu theo từng XPath
    for key, xpath in xpath_tweet.items():
        try:
            # Tìm phần tử bằng XPath và lấy nội dung text
            element = tweet.find_element(By.XPATH, xpath)

            if key == 'content':
                tweet_data[key] = []  # Khởi tạo là một danh sách rỗng
                list_spans = element.find_elements(By.CSS_SELECTOR, 'span')
                for span in list_spans:
                    text = span.text if not span.find_element(By.CLASS_NAME, 'a') else None
                    tweet_data[key].append(text)

            if key == 'media':
                img_element = element.find_element(By.TAG_NAME, 'img')
                tweet_data[key] = img_element.get_attribute('src') if img_element else None
            else:
                tweet_data[key] = utils.convert_to_number(element.text)
            
            if key == 'create_at':
                # Loại bỏ ký tự không mong muốn (bao gồm cả "·")
                raw_text = element.text.replace('·', '').strip()

                 # Chuyển đổi định dạng thời gian
                try:
                    timestamp = datetime.strptime(raw_text, "%I:%M %p %b %d, %Y").strftime('%Y-%m-%d %H:%M:%S')
                    tweet_data[key] = timestamp
                except ValueError:
                    tweet_data[key] = None  # Nếu không thể chuyển đổi thời gian, gán None

        except:
            tweet_data[key] = None  # Gán None nếu không tìm thấy
    print(tweet_data)
    print(json.dumps(tweet_data, indent=4, ensure_ascii=False))

except Exception as e:
    print(str(e))


# Đóng trình duyệt
driver.quit()