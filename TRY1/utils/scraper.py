import uuid
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import random
from ..config.config import (
    TWITTER_USERNAME,
    TWITTER_PASSWORD,
    PROXYMESH_USERNAME,
    PROXYMESH_PASSWORD,
    PROXYMESH_ENDPOINTS
)

class TwitterScraper:
    def __init__(self):
        self.proxy = None
        self.driver = None
        
    def setup_proxy(self):
        """Set up a random proxy from ProxyMesh"""
        proxy_endpoint = random.choice(PROXYMESH_ENDPOINTS)
        self.proxy = f"http://{PROXYMESH_USERNAME}:{PROXYMESH_PASSWORD}@{proxy_endpoint}"
        return self.proxy

    def setup_driver(self):
        """Initialize Selenium WebDriver with proxy"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(f'--proxy-server={self.proxy}')
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def login_to_twitter(self):
        """Login to Twitter"""
        self.driver.get("https://twitter.com/login")
        
        # Wait for and fill username
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        username_field.send_keys(TWITTER_USERNAME)
        username_field.submit()

        # Wait for and fill password
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.submit()

    def get_trending_topics(self):
        """Scrape top 5 trending topics"""
        # Wait for trending section
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='What's happening']"))
        )
        
        # Get trending topics
        trends = self.driver.find_elements(
            By.XPATH,
            "//div[text()='What's happening']/following::div[contains(@class, 'trend-item')]"
        )[:5]
        
        return [trend.text for trend in trends]

    def scrape(self):
        """Main scraping function"""
        try:
            self.setup_proxy()
            self.setup_driver()
            self.login_to_twitter()
            
            trends = self.get_trending_topics()
            
            result = {
                '_id': str(uuid.uuid4()),
                'trends': trends,
                'timestamp': datetime.now(),
                'ip_address': self.proxy
            }
            
            return result
            
        finally:
            if self.driver:
                self.driver.quit()