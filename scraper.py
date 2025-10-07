import json
from plyer import notification
from scrapers.sportsshoes_scraper import scrape_sportsshoes
from scrapers.runnea_scraper import scrape_runnea

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def send_alert(product_name, price, source):
    notification.notify(
        title="Product Alert!",
        message=f"{product_name} is available for £{price} on {source}!",
        timeout=10
    )

def main():
    config = load_config()

    # ✅ SportShoes
    print(f"\n🔍 Checking {config['product_name']} on SportShoes...")
    sportsshoes_url = config['urls']['sportsshoes']
    result_ss = scrape_sportsshoes(sportsshoes_url, config['target_price'], config['size'])

    if result_ss:
        print(f"✅ Match found: {config['product_name']} at £{result_ss['price']} (SportShoes)")
        send_alert(config['product_name'], result_ss['price'], "SportShoes")
    else:
        print("❌ No match found on SportShoes.")

    # ✅ Runnea
    print(f"\n🔍 Checking {config['product_name']} on Runnea...")
    runnea_url = config['urls']['runnea']
    result_runnea = scrape_runnea(runnea_url, config['target_price'], config['size'])

    if result_runnea:
        print(f"✅ Match found: {config['product_name']} at £{result_runnea['price']} (Runnea)")
        send_alert(config['product_name'], result_runnea['price'], "Runnea")
    else:
        print("❌ No match found on Runnea.")

if __name__ == "__main__":
    main()


