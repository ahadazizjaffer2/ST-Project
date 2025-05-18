from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# Setup
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

try:
    # Step 1: Open the website and navigate to a product category
    driver.get("https://automationteststore.com/")
    time.sleep(2)

    # Example: Click "Hair Care"
    driver.find_element(By.LINK_TEXT, "HAIR CARE").click()
    time.sleep(2)

    # Step 2: Find and select "Price: Low to High" from sort dropdown
    sort_dropdown = driver.find_element(By.ID, "sort")
    sort_dropdown.find_element(By.XPATH, "//option[contains(text(), 'Price Low > High')]").click()
    time.sleep(3)

    # Extract product prices (handle both regular and special prices)
    price_elements = driver.find_elements(By.CSS_SELECTOR, ".productinfo .price, .productinfo .pricetag .price")
    price_values = []

    for price_el in price_elements:
        price_text = price_el.text.strip().replace("$", "").split()[0]
        try:
            price_float = float(price_text)
            price_values.append(price_float)
        except:
            continue  # skip if price can't be converted

    print("Extracted Prices:", price_values)

    # Assert that prices are sorted ascending
    assert price_values == sorted(price_values), "Prices are not sorted correctly"
    print("TC08 Passed: Products are sorted from Low to High")

except Exception as e:
    print("TC08 Failed:", e)

finally:
    driver.quit()