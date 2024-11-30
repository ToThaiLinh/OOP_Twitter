import os
import json

class TokenManager:
    TOKEN_FILE = "auth_token.json"

    @staticmethod
    def save_token(token):
        """Lưu token vào file"""
        with open(TokenManager.TOKEN_FILE, "w") as file:
            json.dump({"auth_token": token}, file)

    @staticmethod
    def load_token():
        """Tải token từ file nếu có"""
        if os.path.exists(TokenManager.TOKEN_FILE):
            with open(TokenManager.TOKEN_FILE, "r") as file:
                data = json.load(file)
                return data.get("auth_token")
        return None

class Converter:
    @staticmethod
    def convert_to_number(text):
        """
        Hàm chuyển đổi số dạng '12K', '12M' thành số thực.
        """
        try:
            text = text.replace(',', '.')

            if text.endswith('K'):
                return float(text[:-1]) * 1_000
            elif text.endswith('M'):
                return float(text[:-1]) * 1_000_000
            else:
                return float(text)
        except ValueError:
            return None
