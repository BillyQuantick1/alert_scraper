import requests
from bs4 import BeautifulSoup

def scrape_sportsshoes(product_url, target_price, target_size):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(product_url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # ✅ Extract price
    price_tag = soup.find('h5', class_='chakra-heading css-28v80p')
    if not price_tag:
        print("Price not found.")
        return None

    price_text = price_tag.text.strip().replace('£', '')
    try:
        price = float(price_text)
        print(f"✅ Detected price: £{price}")
    except ValueError:
        print("Could not parse price.")
        return None

    # ✅ Extract sizes from <p> tags
    size_tags = soup.find_all('p', class_='chakra-text css-1fp272q')
    available_sizes = [tag.text.strip() for tag in size_tags]
    print(f"👟 Available sizes: {available_sizes}")

    # ✅ Exact match logic
    if target_size in available_sizes and price <= target_price:
        return {
            "price": price,
            "size": target_size,
            "available": True
        }
    else:
        return None
