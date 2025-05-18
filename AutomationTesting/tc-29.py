from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Replace with a valid registered user
valid_username = "ahadaziz"
valid_password = "KzU77@fnuQrPj7x"

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Log in
    driver.get("https://automationteststore.com/")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login or register").click()
    time.sleep(2)

    driver.find_element(By.ID, "loginFrm_loginname").send_keys(valid_username)
    driver.find_element(By.ID, "loginFrm_password").send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, "button[title='Login']").click()
    time.sleep(3)

    # Step 2: Go to 'Edit Account' section
    driver.find_element(By.LINK_TEXT, "Edit account details").click()
    time.sleep(2)

    # Step 3: Verify profile fields are visible
    firstname = driver.find_element(By.ID, "AccountFrm_firstname").get_attribute("value")
    email = driver.find_element(By.ID, "AccountFrm_email").get_attribute("value")

    assert firstname and email
    print(f"✅ TC29 Passed: Profile information loaded. Name: {firstname}, Email: {email}")

except Exception as e:
    print("❌ TC29 Failed:", e)

finally:
    driver.quit()
