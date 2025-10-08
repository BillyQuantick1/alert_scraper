import json
from plyer import notification
from scrapers.sportsshoes_scraper import scrape_sportsshoes
from scrapers.runnea_scraper import scrape_runnea
from scrapers.achilles_scraper import scrape_achilles_heel  # ✅ NEW

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def send_local_notification(product_name, price, source):
    notification.notify(
        title="Product Alert!",
        message=f"{product_name} is available for £{price} on {source}!",
        timeout=10
    )

def main():
    config = load_config()
    product_name = config['product_name']
    target_price = config['target_price']
    target_size = config['size']

    # ✅ SportShoes
    print(f"\n🔍 Checking {product_name} on SportShoes...")
    result_ss = scrape_sportsshoes(config['urls']['sportsshoes'], target_price, target_size)
    if result_ss:
        print(f"✅ Match found: {product_name} at £{result_ss['price']} (SportShoes)")
        send_local_notification(product_name, result_ss['price'], "SportShoes")
    else:
        print("❌ No match found on SportShoes.")

    # ✅ Runnea
    print(f"\n🔍 Checking {product_name} on Runnea...")
    result_runnea = scrape_runnea(config['urls']['runnea'], target_price, target_size)
    if result_runnea:
        print(f"✅ Match found: {product_name} at £{result_runnea['price']} (Runnea)")
        send_local_notification(product_name, result_runnea['price'], "Runnea")
    else:
        print("❌ No match found on Runnea.")

    # ✅ Achilles Heel
    print(f"\n🔍 Checking {product_name} on Achilles Heel...")
    achilles_urls = config['urls']['achilles_heel']
    result_achilles = scrape_achilles_heel(achilles_urls, target_price, target_size)
    if result_achilles:
        print(f"✅ Match found: {product_name} at £{result_achilles['price']} (Achilles Heel)")
        send_local_notification(product_name, result_achilles['price'], "Achilles Heel")
    else:
        print("❌ No match found on Achilles Heel.")

if __name__ == "__main__":
    main()




