from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

options = Options()
options.add_argument("--start-maximized")

def test_add_multiple_quantities():
    driver = webdriver.Chrome(options=options)
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
        
        driver.save_screenshot("tc36_product_page.png")
        logger.info("Screenshot of product page saved as tc36_product_page.png")
        
        # Set quantity to 3
        quantity_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "product_quantity"))
        )
        quantity_input.clear()
        quantity_input.send_keys("3")
        logger.info("Set quantity to 3")
        
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
        
        # Add to Cart
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
        
        # Verify quantity in cart
        cart_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "cart"))
        )
        cart_link.click()
        
        quantity_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table-bordered input[name^='quantity']"))
        )
        assert quantity_input.get_attribute("value") == "3", \
            f"Expected quantity 3, but found {quantity_input.get_attribute('value')}"
        logger.info("TC36: Successfully added 3 units to cart")
        
    except Exception as e:
        logger.error(f"TC36 Failed: {str(e)}")
        driver.save_screenshot("tc36_error.png")
        logger.info("Screenshot saved as tc36_error.png")
        raise
    
    finally:
        time.sleep(2)
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    test_add_multiple_quantities()