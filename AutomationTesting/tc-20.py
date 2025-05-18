from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Go to the homepage and click "Login or register"
    driver.get("https://automationteststore.com/")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login or register").click()
    time.sleep(2)

    # Step 2: Click "Continue" to go to registration form
    driver.find_element(By.XPATH, "//button[@title='Continue']").click()
    time.sleep(2)

    # Step 3: Fill form with invalid email format
    driver.find_element(By.ID, "AccountFrm_firstname").send_keys("Test")
    driver.find_element(By.ID, "AccountFrm_lastname").send_keys("User")
    driver.find_element(By.ID, "AccountFrm_email").send_keys("abc@com")  # Invalid email
    driver.find_element(By.ID, "AccountFrm_telephone").send_keys("1234567890")
    driver.find_element(By.ID, "AccountFrm_address_1").send_keys("123 Street")
    driver.find_element(By.ID, "AccountFrm_city").send_keys("Testville")
    driver.find_element(By.ID, "AccountFrm_zone_id").send_keys("Alabama")
    driver.find_element(By.ID, "AccountFrm_postcode").send_keys("12345")
    driver.find_element(By.ID, "AccountFrm_country_id").send_keys("United States")
    driver.find_element(By.ID, "AccountFrm_loginname").send_keys(f"testuser{random.randint(1000,9999)}")
    driver.find_element(By.ID, "AccountFrm_password").send_keys("Test@1234")
    driver.find_element(By.ID, "AccountFrm_confirm").send_keys("Test@1234")
    driver.find_element(By.ID, "AccountFrm_agree").click()

    # Step 4: Submit the form
    driver.find_element(By.CSS_SELECTOR, "button[title='Continue']").click()
    time.sleep(2)

    # Step 5: Check for email validation error
    error_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "email" in error_message.lower()
    print("TC20 Passed: Invalid email format was correctly flagged.")

except Exception as e:
    print("TC20 Failed:", e)

finally:
    driver.quit()
