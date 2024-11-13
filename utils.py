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