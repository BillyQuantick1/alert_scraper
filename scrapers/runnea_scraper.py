from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def scrape_runnea(product_url, target_price, target_size):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.get(product_url)

    try:
        # ✅ Extract price
        price_element = driver.find_element(By.CLASS_NAME, "label-price")
        price_text = price_element.text.strip().replace("£", "")
        price = float(price_text)
        print(f"✅ Detected price: £{price}")
    except Exception as e:
        print("Price not found.")
        driver.quit()
        return None

    try:
        # ✅ Extract sizes
        size_elements = driver.find_elements(By.CLASS_NAME, "enlaceofuscadoPills")
        available_sizes = [el.text.strip() for el in size_elements if el.text.strip()]
        print(f"👟 Available sizes: {available_sizes}")
    except Exception as e:
        print("Sizes not found.")
        driver.quit()
        return None

    driver.quit()

    # ✅ Match logic
    if target_size in available_sizes and price <= target_price:
        return {
            "price": price,
            "size": target_size,
            "available": True
        }
    else:
        return None


