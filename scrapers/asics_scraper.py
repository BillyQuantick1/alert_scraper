import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_asics(product_url, target_price, target_size):
    options = uc.ChromeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117 Safari/537.36")

    driver = uc.Chrome(options=options)
    driver.get(product_url)

    price = None
    available_sizes = []

    # ✅ Extract price with explicit wait
    try:
        wait = WebDriverWait(driver, 10)
        price_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='product-price']")))
        price_text = price_element.text.strip().replace("£", "").replace(",", "")
        price = float(price_text)
        print(f"✅ ASICS price: £{price}")
    except Exception as e:
        print("❌ Price not found.")

    # ✅ Extract available sizes
    try:
        time.sleep(2)  # slight delay for size buttons
        size_elements = driver.find_elements(By.CSS_SELECTOR, ".product-size-selector .size")
        available_sizes = [
            el.text.strip()
            for el in size_elements
            if el.get_attribute("aria-disabled") != "true"
        ]
        print(f"👟 ASICS sizes: {available_sizes}")
    except Exception as e:
        print("❌ Sizes not found.")

    driver.quit()

    # ✅ Match logic
    if price is not None and target_size in available_sizes and price <= target_price:
        return {
            "price": price,
            "size": target_size,
            "available": True
        }
    else:
        return None
