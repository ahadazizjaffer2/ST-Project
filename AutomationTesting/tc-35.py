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
driver = webdriver.Chrome(options=options)
driver.maximize_window()

def test_add_single_product_to_cart():

    
    try:
        # Step 1: Navigate to the website
        logger.info("Navigating to https://automationteststore.com/")
        driver.get("https://automationteststore.com/")
        
        # Debug: Print page title
        logger.info(f"Page title: {driver.title}")
        
        # Handle potential cookie pop-up
        try:
            cookie_accept = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".cc-btn.cc-allow"))
            )
            cookie_accept.click()
            logger.info("Accepted cookie consent")
        except TimeoutException:
            logger.info("No cookie consent pop-up found")
        
        # Step 2: Navigate to any category or featured products
        product = None
        try:
            # Try selecting a category from navigation
            nav_links = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.nav-items > li > a"))
            )
            logger.info(f"Found {len(nav_links)} navigation links")
            nav_links[1].click()  # Select second link to avoid "Home"
            
            # Select first product
            product = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-grid-item .prdocutname"))
            )
        except TimeoutException:
            logger.warning("No categories found, trying featured products")
            # Fallback to featured products on homepage
            products = WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".thumbnails .prdocutname"))
            )
            product = products[0]  # Select first featured product
            logger.info("Selected first featured product")
        
        product_name = product.text.strip()
        logger.info(f"Selected product: {product_name}")
        product.click()
        
        # Save screenshot of product page
        driver.save_screenshot("tc35_product_page.png")
        logger.info("Screenshot of product page saved as tc35_product_page.png")
        
        # Step 3: Handle potential product options
        try:
            # Check for select dropdown (e.g., size, color)
            option_select = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "select[name^='option']"))
            )
            option_select.click()
            # Select first available option
            first_option = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name^='option'] option:nth-child(2)"))
            )
            first_option.click()
            logger.info("Selected product option")
        except TimeoutException:
            logger.info("No product options found, proceeding to add to cart")
        
        # Step 4: Add to Cart with multiple selectors
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
            raise Exception("Add to Cart button not found with any selector")
        
        # Step 5: Verify product in cart
        cart_link = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "cart"))
        )
        cart_link.click()
        
        cart_item = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".table-bordered .align_left a"))
        )
        cart_item_name = cart_item.text.strip()
        assert product_name.lower() in cart_item_name.lower(), \
            f"Product {product_name} not found in cart, found {cart_item_name}"
        logger.info("TC35: Product successfully added to cart")
        
    except Exception as e:
        logger.error(f"TC35 Failed: {str(e)}")
        driver.save_screenshot("tc35_error.png")
        logger.info("Screenshot saved as tc35_error.png")
        raise
    
    finally:
        time.sleep(2)
        driver.quit()
        logger.info("Browser closed")

if __name__ == "__main__":
    test_add_single_product_to_cart()