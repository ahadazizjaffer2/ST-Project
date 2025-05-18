from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

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

    # Step 2: Go to "Edit Account"
    driver.find_element(By.LINK_TEXT, "Edit account details").click()
    time.sleep(2)

    # Step 3: Change the first name
    new_first_name = f"Test{random.randint(100,999)}"
    firstname_input = driver.find_element(By.ID, "AccountFrm_firstname")
    firstname_input.clear()
    firstname_input.send_keys(new_first_name)

    # Step 4: Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[title='Continue']").click()
    time.sleep(2)

    # Step 5: Verify the success message
    success_msg = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "success" in success_msg.lower()
    print(f"✅ TC30 Passed: First name updated to '{new_first_name}'.")

except Exception as e:
    print("❌ TC30 Failed:", e)

finally:
    driver.quit()
