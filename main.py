import login
import crawl
from dotenv import load_dotenv
import os

load_dotenv()
# Nhập thông tin đăng nhập Twitter
username = os.getenv('USERNAME')  # Thay bằng tên người dùng của bạn
password = os.getenv('PASSWORD')  # Thay bằng mật khẩu của bạn

# Lấy hoặc tải lại auth_token
auth_token = login.login_and_get_token(username, password)

# Nếu lấy được token, tiếp tục tìm bài viết
if auth_token:
    crawl.fetch_blockchain_tweets(auth_token)
else:
    print("Không thể đăng nhập và lấy token.")
