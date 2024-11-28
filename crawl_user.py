from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
import json
import utils
from datetime import datetime

auth_token = '115b13796cb12c39092b93d1286a0b7078170ddf'

driver = webdriver.Chrome()
driver.get('https://x.com')

driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })

time.sleep(5)

driver.get("https://x.com/elonmusk")
time.sleep(5)

xpath_user = {
    'user_id' : './div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/span',
    'username' : './div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/span/span[1]',
    'role': './div/div/div/div/div/div[3]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/span/span[2]/span[1]/span[1]/div',
    'joined_at' : './div/div/div/div/div/div[3]/div/div/div/div/div[4]/div/span/span',
    'following': './div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span',
    'follower' : './div/div/div/div/div/div[3]/div/div/div/div/div[5]/div[1]/a/span[1]/span' ,
    'posts_cnt': './div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/div'
}

def crawl_user(driver, xpath_user):
    try:
        main_element = driver.find_element(By.TAG_NAME, "main")
        user_data = {}

        # Tìm và trích xuất dữ liệu theo từng XPath
        for key, xpath in xpath_user.items():
            try:
                element = main_element.find_element(By.XPATH, xpath)
                if key == "role":
                   
                    try:
                        role_element = main_element.find_element(By.XPATH, xpath)
                        user_data[key] = 'KOL'  
                    except:
                        user_data[key] = 'User'  
                elif key == 'following' or key == 'follower':
                    user_data[key] = utils.convert_to_number(element.text)
                elif key == 'posts_cnt':
                    text_cnt = element.text.split()[0]
                    user_data[key] = utils.convert_to_number(text_cnt)
                elif key == 'joined_at':
                    words = element.text.split(" ")
                    text_time = " ".join(words[-2:])
                    user_data[key] = datetime.strptime(text_time, "%B %Y").strftime('%Y-%m-%d %H:%M:%S')
                else:
                   
                    user_data[key] = element.text
            except:
                user_data[key] = None  

        print(json.dumps(user_data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(str(e))

crawl_user(driver, xpath_user)

driver.quit()