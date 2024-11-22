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


try:
    main_element = driver.find_element(By.TAG_NAME, "main")
    print('da tim thay main')
    user_data = {}

    # Tìm và trích xuất dữ liệu theo từng XPath
    for key, xpath in xpath_user.items():
        try:
            if key == "role":
                # Kiểm tra sự tồn tại của tick xanh
                try:
                    role_element = main_element.find_element(By.XPATH, xpath)
                    user_data[key] = 'KOL'  # Gán 2 nếu có tick xanh (KOL)
                except:
                    user_data[key] = 'User'  # Gán 1 nếu không có tick xanh (User)
            else:
                # Tìm phần tử bằng XPath và lấy nội dung text
                element = main_element.find_element(By.XPATH, xpath)
                user_data[key] = element.text
        except:
            user_data[key] = None  # Gán None nếu không tìm thấy

    # In dữ liệu đã trích xuất
    print(json.dumps(user_data, indent=4, ensure_ascii=False))
except Exception as e:
    print(str(e))

# Đóng trình duyệt
driver.quit()