import json
from plyer import notification
from sportsshoes_scraper import scrape_sportsshoes

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def send_alert(product_name, price):
    notification.notify(
        title="Product Alert!",
        message=f"{product_name} is available for £{price}!",
        timeout=10
    )

def main():
    config = load_config()
    product_url = "https://www.sportsshoes.com/product/asi16116/asics-megablast-running-shoes---aw25"

    result = scrape_sportsshoes(product_url, config['target_price'], config['size'])

    if result:
        print(f"✅ Match found: {config['product_name']} at £{result['price']}")
        send_alert(config['product_name'], result['price'])
    else:
        print("❌ No match found.")

if __name__ == "__main__":
    main()

