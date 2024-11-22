xpath_tweet = {
    #'tweet_id': '',
    'create_at' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[1]/a/time',
    'content' : '',
    'media' : '',
    'comment_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[1]/button/div/div[2]/span/span/span',
    'repost_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[2]/button/div/div[2]/span/span/span',
    'like_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[5]/div/div/div[3]/button/div/div[2]/span/span/span',
    'view_cnt' : './div/div/div/div/div/section/div/div/div[1]/div/div/article/div/div/div[3]/div[4]/div/div[1]/div/div[3]/span/div/span/span/span'
}

from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
import json

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })
time.sleep(10)

driver.get("https://x.com/King_SpawN2010/status/1857776405175492700")
time.sleep(10)


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
            tweet_data[key] = element.text
        except:
            tweet_data[key] = None  # Gán None nếu không tìm thấy
    print(json.dumps(tweet_data, indent=4, ensure_ascii=False))

except Exception as e:
    print(str(e))


# Đóng trình duyệt
driver.quit()