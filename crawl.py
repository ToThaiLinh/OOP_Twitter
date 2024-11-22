from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time


# Danh sách các hashtag liên quan đến blockchain
hashtags = [
    "blockchain", "crypto", "cryptocurrency", "bitcoin", "ethereum", 
    "DeFi", "NFT", "web3", "blockchaintechnology", "altcoin", 
    "smartcontracts", "digitalassets", "cryptoart", "metaverse",
    "cryptoexchange", "token", "cryptotrading", "cryptoinvestor",
    "blockchainnews", "cryptoworld", "blockchainrevolution", 
    "DAO", "dapps", "cryptomarket", "cryptonews"
]


def fetch_blockchain_tweets(auth_token):
    # Khởi tạo trình duyệt
    driver = webdriver.Chrome()
    
    # Đặt auth_token vào cookie để duy trì phiên đăng nhập
    driver.get("https://x.com")  # Mở trang chính để đặt cookie
    driver.add_cookie({
        "name": "auth_token",
        "value": auth_token,
        "domain": ".x.com"
    })
    
    # Duyệt qua từng hashtag trong danh sách
    for tag in hashtags[0:1]:
        # Mở trang hashtag tương ứng
        driver.get(f"https://x.com/hashtag/{tag}")
        driver.implicitly_wait(20)

        # Cuộn xuống để tải thêm nội dung
        for _ in range(3):  # Có thể điều chỉnh số lần cuộn
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randint(5, 10))

        # Lấy danh sách các bài tweet
        tweets = driver.find_elements(By.CSS_SELECTOR, "article")
        
        # In nội dung các bài viết
        print(f"Hashtag #{tag}:")
        for i, tweet in enumerate(tweets):
            try:
                content = tweet.find_element(By.CSS_SELECTOR, "div[lang]").text
            except Exception as e:
                print(f'Khong the lay bai viet #{i + 1}')
                print(f'Lỗi {str(e)}')
                continue
        print("\n" + "="*50 + "\n")  # Phân cách giữa các hashtag

    # Đóng trình duyệt
    driver.quit()

fetch_blockchain_tweets('115b13796cb12c39092b93d1286a0b7078170ddf')