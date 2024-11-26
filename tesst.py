from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
 
driver = webdriver.Chrome()
 
try:
    driver.get("https://twitter.com/")
    time.sleep(3)  
   
    tweet_url = "https://x.com/elonmusk/status/1859472839792820276"
    driver.get(tweet_url)
    time.sleep(5)  
 
    tweet_text_xpath = "//div[@data-testid='tweetText']"
    tweet_content = driver.find_element(By.XPATH, tweet_text_xpath).text
 
    print("Nội dung bài tweet:", tweet_content)
 
finally:
    driver.quit()