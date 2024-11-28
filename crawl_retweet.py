from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from datetime import datetime
import uuid

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

driver.get("https://x.com/AMAZlNGNATURE/status/1861508866665484498/retweets")
time.sleep(5)

for _ in range(3):  
    driver.execute_script("window.scrollTo(0, 500)")
    time.sleep(3)

element_section = driver.find_element(By.TAG_NAME, 'section')




retweet_xpath = {
    'user_id': './div/div/div[{i}]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span',
    'content': './div/div/div[{i}]/div/div/button/div/div[2]/div[2]/span'
}
repost = []
for i in range(1, 10, 1):
    retweet_data = {}
    try:
        retweet_data['respost_id'] = str(uuid.uuid4())
        retweet_data['user_id'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[1]/div[1]/div/div[2]/div/a/div/div/span').text
        retweet_data['id'] = driver.current_url.split('/')[-2]
        retweet_data['type'] = 'retweet'
        retweet_data['content'] = element_section.find_element(By.XPATH, f'./div/div/div[{i}]/div/div/button/div/div[2]/div[2]/span').text
    except Exception as e:
        print(str(e))
        retweet_data = None
    repost.append(retweet_data)

print(json.dumps(repost, indent=4, ensure_ascii=False))