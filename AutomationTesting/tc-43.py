from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

options = Options()
options.add_argument("--start-maximized")

# Custom Expected Condition to wait for element with specific text
class text_to_be_present_in_element:
    def __init__(self, locator, text_):
        self.locator = locator
        self.text = text_

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            return self.text in element.text
        except:
            return False

def test_complete_checkout_with_valid_info():
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()
    
    try:
        logger.info("Navigating to https://automationteststore.com/")
        driver.get("https://automationteststore.com/")
        logger.info(f"Page title: {driver.title}")
        
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc-btn.cc-allow"))
            )
            cookie_accept.click()
            logger.info("Accepted cookie consent")
        except TimeoutException:
            logger.info("No cookie consent pop-up found")
        
        product = None
        try:
            nav_links = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.nav-items > li > a"))
            )
            logger.info(f"Found {len(nav_links)} navigation links")
            nav_links[1].click()
            product = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-grid-item .prdocutname"))
            )
        except TimeoutException:
            logger.warning("No categories found, trying featured products")
            products = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnails .prdocutname"))
            )
            product = products[0]
            logger.info("Selected first featured product")
        
        product_name = product.text.strip()
        logger.info(f"Selected product: {product_name}")
        product.click()
        
        driver.save_screenshot("tc43_product_page.png")
        logger.info("Screenshot of product page saved as tc43_product_page.png")
        
        # Handle potential product options
        try:
            option_select = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[name^='option']"))
            )
            option_select.click()
            first_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name^='option'] option:nth-child(2)"))
            )
            first_option.click()
            logger.info("Selected product option")
        except TimeoutException:
            logger.info("No product options found")
        
        # Add to cart
        add_to_cart_button = None
        selectors = [
            (By.CSS_SELECTOR, ".cart"),
            (By.CSS_SELECTOR, "button[title='Add to Cart']"),
            (By.XPATH, "/html/body/div/div[2]/div/div[2]/div/div[1]/div/div[2]/div/div/div[2]/form/fieldset/div[4]/ul/li/a")
        ]
        for by, selector in selectors:
            try:
                add_to_cart_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((by, selector))
                )
                logger.info(f"Found Add to Cart button with {by}: {selector}")
                break
            except TimeoutException:
                logger.warning(f"Selector {by}: {selector} not found")
        
        if add_to_cart_button:
            add_to_cart_button.click()
            logger.info("Clicked Add to Cart")
        else:
            raise Exception("Add to Cart button not found")
        
        # Go to cart
        cart_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "cart"))
        )
        cart_link.click()
        
        # Click checkout
        checkout_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "cart_checkout1"))
        )
        checkout_button.click()
        
        # Select guest checkout
        guest_radio = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "accountFrm_accountguest"))
        )
        guest_radio.click()
        logger.info("Selected guest checkout")
        
        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Continue']"))
        )
        continue_button.click()
        
        # Save screenshot of checkout page
        driver.save_screenshot("tc43_checkout_page.png")
        logger.info("Screenshot of checkout page saved as tc43_checkout_page.png")
        
        # Fill checkout fields
        text_fields = {
            "guestFrm_firstname": "John",
            "guestFrm_lastname": "Doe",
            "guestFrm_email": f"john.doe{int(time.time())}@example.com",
            "guestFrm_telephone": "1234567890",
            "guestFrm_address_1": "123 Main St",
            "guestFrm_city": "New York",
            "guestFrm_postcode": "10001"
        }
        
        # Handle text input fields
        for field, value in text_fields.items():
            input_field = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, field))
            )
            input_field.clear()
            input_field.send_keys(value)
            logger.info(f"Filled text field {field}")
        
        # Handle country dropdown
        country_select = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "guestFrm_country_id"))
        )
        Select(country_select).select_by_value("223")  # United States
        logger.info("Selected country: United States")
        
        # Save screenshot after selecting country
        driver.save_screenshot("tc43_country_selected.png")
        logger.info("Screenshot after country selection saved as tc43_country_selected.png")
        
        # Wait for zone dropdown to populate and log available options
        try:
            zone_select = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.ID, "guestFrm_zone_id"))
            )
            zone_options = zone_select.find_elements(By.TAG_NAME, "option")
            available_zones = [(opt.get_attribute("value"), opt.text) for opt in zone_options if opt.get_attribute("value")]
            logger.info(f"Available zones: {available_zones}")
            
            # Try selecting New York by value
            try:
                Select(zone_select).select_by_value("3655")  # Correct value for New York
                logger.info("Selected zone: New York (by value 3655)")
            except NoSuchElementException:
                logger.warning("Zone value '3655' not found, trying CSS selector")
                # Try CSS selector for New York (nth-child)
                try:
                    new_york_option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "#guestFrm_zone_id > option:nth-child(44)"))
                    )
                    new_york_value = new_york_option.get_attribute("value")
                    Select(zone_select).select_by_value(new_york_value)
                    logger.info(f"Selected zone: New York (by CSS selector, value {new_york_value})")
                except TimeoutException:
                    logger.warning("CSS selector '#guestFrm_zone_id > option:nth-child(44)' not found, selecting first available zone")
                    for value, text in available_zones:
                        if value and value != "FALSE":
                            Select(zone_select).select_by_value(value)
                            logger.info(f"Selected fallback zone: {text} (value {value})")
                            break
                    else:
                        raise Exception("No valid zone options available")
        except TimeoutException:
            logger.error("Zone dropdown did not populate within 30 seconds")
            raise
        
        continue_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Continue']"))
        )
        continue_button.click()
        
        # Save screenshot before confirm order
        driver.save_screenshot("tc43_confirm_page.png")
        logger.info("Screenshot before confirm order saved as tc43_confirm_page.png")
        
        # Confirm order
        confirm_selectors = [
            (By.ID, "checkout_btn"),
            (By.CSS_SELECTOR, ".btn-orange.pull-right[title='Confirm Order']"),
            (By.XPATH, "//button[contains(text(), 'Confirm Order')]")
        ]
        
        confirm_button = None
        for by, selector in confirm_selectors:
            try:
                confirm_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((by, selector))
                )
                logger.info(f"Found Confirm Order button with {by}: {selector}")
                break
            except TimeoutException:
                logger.warning(f"Confirm selector {by}: {selector} not found")
        
        if confirm_button:
            confirm_button.click()
            logger.info("Clicked Confirm Order")
        else:
            raise Exception("Confirm Order button not found")
        
        # Verify order confirmation
        confirmation_selectors = [
            (By.CSS_SELECTOR, "span.maintext"),  # Target the span with class maintext
            (By.XPATH, "//span[contains(text(), 'Your Order Has Been Processed')]")
        ]
        
        confirmation = None
        for by, selector in confirmation_selectors:
            try:
                confirmation = WebDriverWait(driver, 30).until(
                    text_to_be_present_in_element((by, selector), "YOUR ORDER HAS BEEN PROCESSED!")
                )
                confirmation = driver.find_element(by, selector)
                confirmation_text = confirmation.text.strip()
                logger.info(f"Found confirmation text with {by}: {selector}, text: '{confirmation_text}'")
                break
            except TimeoutException:
                logger.warning(f"Confirmation selector {by}: {selector} not found or text not present")
        
        if confirmation:
            assert "YOUR ORDER HAS BEEN PROCESSED!" in confirmation_text, f"Order confirmation not displayed, found: '{confirmation_text}'"
            logger.info("TC43: Order successfully placed")
        else:
            # Log all .maintext elements for debugging
            maintext_elements = driver.find_elements(By.CSS_SELECTOR, ".maintext")
            maintext_texts = [elem.text.strip() for elem in maintext_elements]
            logger.info(f"All .maintext elements: {maintext_texts}")
            raise Exception("Confirmation text 'Your Order Has Been Processed' not found in any selector")
        
    except Exception as e:
        logger.error(f"TC43 Failed: {str(e)}")
        driver.save_screenshot("tc43_error.png")
        logger.info("Screenshot saved as tc43_error.png")
        raise
    
    finally:
        time.sleep(2)
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    test_complete_checkout_with_valid_info()