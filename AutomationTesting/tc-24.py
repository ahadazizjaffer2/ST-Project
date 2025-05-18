from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

# Use a clearly invalid username and any dummy password
invalid_username = "ahadaziz1"
valid_password = "KzU77@fnuQrPj7x"

try:
    # Step 1: Open website and navigate to login page
    driver.get("https://automationteststore.com/")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login or register").click()
    time.sleep(2)

    # Step 2: Input invalid username and valid password
    driver.find_element(By.ID, "loginFrm_loginname").send_keys(invalid_username)
    driver.find_element(By.ID, "loginFrm_password").send_keys(valid_password)

    # Step 3: Click Login
    driver.find_element(By.CSS_SELECTOR, "button[title='Login']").click()
    time.sleep(2)

    # Step 4: Verify error message is displayed
    error_alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    assert "error" in error_alert.text.lower() or "invalid" in error_alert.text.lower()
    print("✅ TC24 Passed: Error displayed for invalid username.")

except Exception as e:
    print("❌ TC24 Failed:", e)

finally:
    driver.quit()
