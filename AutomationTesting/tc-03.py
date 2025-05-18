from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open the website
    driver.get("https://automationteststore.com/")
    time.sleep(2)

    # Step 2: Find the correct search input field and enter a valid keyword
    search_input = driver.find_element(By.NAME, "filter_keyword")
    search_input.clear()
    search_input.send_keys("shampoo")

    # Step 3: Click the search button (same class and location)
    search_button = driver.find_element(By.CSS_SELECTOR, "div.button-in-search")
    search_button.click()
    time.sleep(2)

    # Step 4: Verify the result contains the keyword
    assert "shampoo" in driver.page_source.lower()
    print("✅ TC03 Passed: Valid keyword search returned results.")

except Exception as e:
    print("❌ TC03 Failed:", e)

finally:
    driver.quit()
