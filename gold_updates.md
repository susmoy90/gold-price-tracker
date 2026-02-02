# gold-price-tracker
Here are the day to day check gold price visualization find and check news bangla.
import requests
import os

def get_gold_price():
    api_key = os.getenv("GOLD_API_KEY") # এটি সিকিউরিটির জন্য গিটহাব সেটিংস থেকে আসবে
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": api_key, "Content-Type": "application/json"}
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    price = data.get('price', 'N/A')
    return f"* **তারিখ:** {data.get('date', 'N/A')} | **দাম:** ${price} USD/Ounce"

def write_to_file(content):
    with open("gold_updates.md", "a", encoding="utf-8") as f:
        f.write(content + "\n")

if __name__ == "__main__":
    new_price = get_gold_price()
    write_to_file(new_price)
