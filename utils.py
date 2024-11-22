import os
import json

TOKEN_FILE = "auth_token.json"

def save_token(token):
    with open(TOKEN_FILE, "w") as file:
        json.dump({"auth_token": token}, file)

def load_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            data = json.load(file)
            return data.get("auth_token")
    return None

def convert_to_number(text):
    """
    Hàm chuyển đổi số dạng '12K', '12M' thành số thực.
    """
    try:
        if text.endswith('K'):
            return float(text[:-1]) * 1_000
        elif text.endswith('M'):
            return float(text[:-1]) * 1_000_000
        else:
            return float(text)
    except ValueError:
        return None  