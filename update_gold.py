import requests
import os

def get_gold_price():
    # গিটহাব সিক্রেটস থেকে এপিআই কি নেওয়া হচ্ছে
    api_key = os.getenv("GOLD_API_KEY")
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {
        "x-access-token": api_key, 
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # দাম এবং কারেন্সি সংগ্রহ
        price = data.get('price', 'N/A')
        price_gram_24k = data.get('price_gram_24k', 'N/A')
        
        return f"### আপডেট: {data.get('date', 'N/A')}\n* **সোনার দাম (আউন্স):** ${price} USD\n* **সোনার দাম (প্রতি গ্রাম ২৪ ক্যারেট):** ${price_gram_24k} USD\n"
    except Exception as e:
        return f"Error fetching data: {e}"

def write_to_file(content):
    # gold_updates.md ফাইলে তথ্য যোগ করা
    with open("gold_updates.md", "a", encoding="utf-8") as f:
        f.write(content + "\n---\n")

if __name__ == "__main__":
    new_data = get_gold_price()
    write_to_file(new_data)
