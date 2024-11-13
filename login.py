from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import utils

def login_and_get_token(username, password):  
    auth_token = utils.load_token()
    if auth_token:
        print(f"Đã sử dụng auth_token đã lưu. Token: {auth_token}")
        return auth_token
    driver = webdriver.Chrome()
    driver.get("https://x.com/login")
    time.sleep(10)

    # Nhập tên người dùng
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(10)

    # Nhập mật khẩu
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    time.sleep(10)

    # Lấy auth_token từ cookie sau khi đăng nhập
    auth_token = None
    for cookie in driver.get_cookies():
        if cookie['name'] == 'auth_token':
            auth_token = cookie['value']
            utils.save_token(auth_token)  # Lưu auth_token để sử dụng sau này
            break

    driver.quit()

    if auth_token:
        print("Đăng nhập thành công và lưu auth_token.")
    else:
        print("Không thể lấy auth_token. Kiểm tra lại thông tin đăng nhập.")
    
    return auth_token
