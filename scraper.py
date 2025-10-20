import json
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from plyer import notification

from scrapers.sportsshoes_scraper import scrape_sportsshoes
from scrapers.runnea_scraper import scrape_runnea
from scrapers.achilles_scraper import scrape_achilles_heel

# Load environment variables from .env file
# Load environment variables from .env file
load_dotenv(dotenv_path="variables.env")

# ✅ Debug print to confirm variable is loaded
print("Loaded ALERT_TO:", os.getenv("ALERT_TO"))


def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def send_local_notification(product_name, price, source):
    notification.notify(
        title="Product Alert!",
        message=f"{product_name} is available for £{price} on {source}!",
        timeout=10
    )

def send_email_alert(product_name, price, source, url):
    msg = EmailMessage()
    try:
        msg['From'] = os.environ['ALERT_FROM']
        msg['To'] = os.environ['ALERT_TO']
        msg['Subject'] = f"{product_name} Alert: £{price} on {source}"
        msg.set_content(f"{product_name} is available for £{price} on {source}!\n\nLink: {url}")

        with smtplib.SMTP('smtp-relay.brevo.com', 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ['BREVO_SMTP_USER'], os.environ['BREVO_SMTP_PASS'])
            smtp.send_message(msg)
            print("📧 Email alert sent successfully!")
    except KeyError as e:
        print(f"⚠️ Missing environment variable: {e}")
    except Exception as e:
        print(f"⚠️ Failed to send email alert: {e}")

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
        url = result_ss.get('url', 'https://sportsshoes.com')
        send_email_alert(product_name, result_ss['price'], "SportShoes", url)
    else:
        print("❌ No match found on SportShoes.")

    # ✅ Runnea
    print(f"\n🔍 Checking {product_name} on Runnea...")
    result_runnea = scrape_runnea(config['urls']['runnea'], target_price, target_size)
    if result_runnea:
        print(f"✅ Match found: {product_name} at £{result_runnea['price']} (Runnea)")
        send_local_notification(product_name, result_runnea['price'], "Runnea")
        url = result_runnea.get('url', 'https://runnea.com')
        send_email_alert(product_name, result_runnea['price'], "Runnea", url)
    else:
        print("❌ No match found on Runnea.")

    # ✅ Achilles Heel
    print(f"\n🔍 Checking {product_name} on Achilles Heel...")
    achilles_urls = config['urls']['achilles_heel']
    result_achilles = scrape_achilles_heel(achilles_urls, target_price, target_size)
    if result_achilles:
        print(f"✅ Match found: {product_name} at £{result_achilles['price']} (Achilles Heel)")
        send_local_notification(product_name, result_achilles['price'], "Achilles Heel")
        url = result_achilles.get('url', 'https://achillesheel.co.uk')
        send_email_alert(product_name, result_achilles['price'], "Achilles Heel", url)
    else:
        print("❌ No match found on Achilles Heel.")

if __name__ == "__main__":
    main()







