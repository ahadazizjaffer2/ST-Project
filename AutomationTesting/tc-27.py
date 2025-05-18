from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
    # Step 1: Open site and log in
    driver.get("https://automationteststore.com/")
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, "Login or register").click()
    time.sleep(2)

    driver.find_element(By.ID, "loginFrm_loginname").send_keys(valid_username)
    driver.find_element(By.ID, "loginFrm_password").send_keys(valid_password)
    driver.find_element(By.CSS_SELECTOR, "button[title='Login']").click()
    time.sleep(3)

    # Step 2: Extract the dynamic username from the "Welcome back" text
    welcome_text = driver.find_element(By.CLASS_NAME, "menu_text").text  # Extract "Welcome back Ahad"
    username = welcome_text.split(" ")[2]  # Get "Ahad" (or dynamic part)

    # Step 3: Hover over the Account Dropdown to reveal the menu
    account_dropdown = driver.find_element(By.CLASS_NAME, "menu_account")
    
    # Create an ActionChain object to hover
    actions = ActionChains(driver)
    actions.move_to_element(account_dropdown).perform()
    time.sleep(2)  # Wait for the dropdown menu to appear

    # Step 4: Check if "Logoff" exists in the dropdown menu
    dropdown_menu = driver.find_element(By.CLASS_NAME, "dropdown-menu")
    logoff_links = dropdown_menu.find_elements(By.PARTIAL_LINK_TEXT, "Logoff")

    if logoff_links:
        print(f"TC27 Passed: Logoff option found in the dropdown for {username}.")
    else:
        print(f"TC27 Failed: Logoff option not found in the dropdown for {username}.")

    # Step 5: Click the Logoff link
    logoff_links[0].click()     
    time.sleep(3)

    login_button = driver.find_element(By.LINK_TEXT, "Login or register")
    
    if login_button.is_displayed():
        print("TC27 Passed: Successfully logged out, 'Login or Register' button is visible.")
    else:
        print("TC27 Failed: 'Login or Register' button not found after logoff.")
except Exception as e:
    print("TC27 Failed:", e)

finally:
    driver.quit()
