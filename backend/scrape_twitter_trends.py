from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from datetime import datetime
import uuid

# ScraperAPI details
SCRAPER_API_KEY = "3a524a447adc01c726dd04d43b57362f"  
SCRAPER_API_URL = f"http://proxy.scraperapi.com:8001/?api_key={SCRAPER_API_KEY}"

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["twitter_trends"]
collection = db["trends"]

def configure_driver_with_proxy():
    # Set up Selenium with ScraperAPI proxy
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    
    # Configure proxy
    proxy = Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    proxy.http_proxy = SCRAPER_API_URL
    proxy.ssl_proxy = SCRAPER_API_URL
    
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    
    # Create WebDriver instance
    driver = webdriver.Chrome(
        service=Service("/path/to/chromedriver"),  # Update with your ChromeDriver path
        options=options,
        desired_capabilities=capabilities
    )
    return driver

def scrape_twitter_trends():
    driver = configure_driver_with_proxy()
    try:
        # Login to Twitter (replace with your credentials)
        driver.get("https://twitter.com/login")
        driver.implicitly_wait(10)
        
        # Enter credentials
        driver.find_element(By.NAME, "text").send_keys("your_username")  # Replace with your Twitter username
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        driver.implicitly_wait(10)
        driver.find_element(By.NAME, "password").send_keys("your_password")  # Replace with your Twitter password
        driver.find_element(By.XPATH, "//span[text()='Log in']").click()
        driver.implicitly_wait(10)
        
        # Scrape trending topics
        driver.get("https://twitter.com/explore/tabs/trending")
        trends = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")[:5]
        trend_names = [trend.text for trend in trends if trend.text]
        
        # Save data to MongoDB
        if trend_names:
            unique_id = str(uuid.uuid4())
            ip_address = SCRAPER_API_URL.split("@")[-1]  # IP fetched via ScraperAPI
            now = datetime.now()
            
            record = {
                "_id": unique_id,
                "trend1": trend_names[0],
                "trend2": trend_names[1],
                "trend3": trend_names[2],
                "trend4": trend_names[3],
                "trend5": trend_names[4],
                "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
                "ip_address": ip_address,
            }
            collection.insert_one(record)
            print("Data saved to MongoDB:", record)
        else:
            print("No trends found.")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_twitter_trends()
