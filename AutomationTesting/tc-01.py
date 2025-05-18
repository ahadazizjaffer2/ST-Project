from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    driver.get("https://automationteststore.com/")

    # Wait for the category menu to be visible
    skincare_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='category&path=43']"))
    )
    skincare_link.click()

    # Wait for the page to load and verify
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".maintext"))
    )
    print("TC01 Passed: Skincare category opened successfully.")

except Exception as e:
    print("TC01 Failed:", e)

finally:
    driver.quit()
