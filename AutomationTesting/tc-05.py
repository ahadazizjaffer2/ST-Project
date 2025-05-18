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

    # Step 2: Locate search bar and enter invalid keyword
    search_input = driver.find_element(By.NAME, "filter_keyword")
    search_input.clear()
    search_input.send_keys("xyzabc")

    # Step 3: Click search
    search_button = driver.find_element(By.CSS_SELECTOR, "div.button-in-search")
    search_button.click()
    time.sleep(2)

    # Step 4: Check for "no results" message
    no_result_element = driver.find_element(By.CSS_SELECTOR, "div.contentpanel")
    assert "There is no product that matches the search criteria." in no_result_element.text
    print("TC05 Passed: No results found message is displayed for invalid keyword.")

except Exception as e:
    print("TC05 Failed:", e)

finally:
    driver.quit()
