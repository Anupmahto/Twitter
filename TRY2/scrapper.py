from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

def scrape_twitter(proxy=None):
    options = Options()
    if proxy:
        options.add_argument(f'--proxy-server={proxy}')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Login to Twitter
        driver.get("https://twitter.com/login")
        
        # Wait for the username field and enter username
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username.send_keys(os.getenv('TWITTER_USERNAME'))
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        
        # Wait for password field and enter password
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password.send_keys(os.getenv('TWITTER_PASSWORD'))
        driver.find_element(By.XPATH, "//span[text()='Log in']").click()
        
        # Check for mobile number input
        try:
            mobile_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "phone_number"))
            )
            mobile_input.send_keys(os.getenv('TWITTER_PHONE'))
            driver.find_element(By.XPATH, "//span[text()='Next']").click()
        except TimeoutException:
            print("Mobile number input not required.")
        
        # Wait for the page to load and fetch trending topics
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='tweet']"))
        )
        
        trending_topics = driver.find_elements(By.XPATH, "//div[@data-testid='tweetText']")
        topics = [topic.text.split('\n')[0] for topic in trending_topics[:5]]
        
        return {
            "id": str(uuid.uuid4()),
            "trends": topics,
            "timestamp": datetime.now().isoformat(),
            "ip_address": proxy if proxy else "local"
        }
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        driver.quit()

if __name__ == "__main__":
    result = scrape_twitter()
    print(result)

