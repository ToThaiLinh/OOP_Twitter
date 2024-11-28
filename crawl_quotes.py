from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time
import json
import Utils.utils as utils
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

driver.get("https://x.com/AMAZlNGNATURE/status/1861508866665484498/quotes")
time.sleep(5)

