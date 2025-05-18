from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Replace these with a valid registered user's credentials
valid_username = "ahadaziz"
valid_password = "KzU77@fnuQrPj7x"

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Navigate to login page
    driver.get("https://automationteststore.com/")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login or register").click()
    time.sleep(2)

    # Step 2: Enter credentials
    driver.find_element(By.ID, "loginFrm_loginname").send_keys(valid_username)
    driver.find_element(By.ID, "loginFrm_password").send_keys(valid_password)

    # Step 3: Click Login
    driver.find_element(By.CSS_SELECTOR, "button[title='Login']").click()
    time.sleep(2)

    # Step 4: Assert login successful
    welcome_text = driver.find_element(By.CLASS_NAME, "heading1").text
    assert "my account" in welcome_text.lower()
    print("TC23 Passed: Logged in successfully with valid credentials.")

except Exception as e:
    print("TC23 Failed:", e)

finally:
    driver.quit()
