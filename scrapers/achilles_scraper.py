from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def scrape_achilles_heel(product_urls, target_price, target_size):
    options = Options()
    options.use_chromium = True
    options.add_argument("--headless")  # ✅ Run silently
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117 Safari/537.36")

    driver = webdriver.Edge(options=options)

    for url in product_urls:
        print(f"🔗 Visiting: {url}")
        driver.get(url)

        try:
            # ✅ Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
            )

            # ✅ Parse page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # ✅ Extract price using regex from sale-price tag
            price_tag = soup.find("sale-price", class_="h6")
            if price_tag:
                match = re.search(r"£\s?(\d+(?:\.\d{1,2})?)", price_tag.text)
                if match:
                    price = float(match.group(1))
                    print(f"✅ Price found: £{price}")
                else:
                    print("❌ Price format not matched.")
                    continue
            else:
                print("❌ Price tag not found.")
                continue
        except Exception as e:
            print(f"❌ Price scraping error: {e}")
            continue

        try:
            # ✅ Extract sizes
            size_elements = soup.select("fieldset[aria-label='Size'] span")
            available_sizes = []
            for el in size_elements:
                text = el.get_text(strip=True)
                if text.replace(".", "").isdigit():
                    available_sizes.append(text)
            print(f"👟 Sizes found: {available_sizes}")
        except Exception as e:
            print(f"❌ Size scraping error: {e}")
            continue

        # ✅ Match logic
        if target_size in available_sizes and price <= target_price:
            driver.quit()
            return {
                "price": price,
                "size": target_size,
                "available": True,
                "url": url
            }

    driver.quit()
    return None




