import json
from plyer import notification

# Load config
def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

# Notify user
def send_alert(product_name, price):
    notification.notify(
        title="Product Alert!",
        message=f"{product_name} is available for £{price}!",
        timeout=10
    )

# Main logic
def main():
    config = load_config()
    print(f"Tracking: {config['product_name']}")
    print(f"Target price: £{config['target_price']}")
    print(f"Size: {config['size']}")

    # Placeholder for scraping logic
    # We'll add real scraping next

if __name__ == "__main__":
    main()
