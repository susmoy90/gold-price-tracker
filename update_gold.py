import requests
import feedparser
import os
import datetime

def get_gold_news():
    # Google News থেকে গোল্ডের খবর আনা
    news_url = "https://news.google.com/rss/search?q=gold+price+market"
    feed = feedparser.parse(news_url)
    
    news_content = "### আজকের সর্বশেষ খবর:\n"
    # সেরা ৫টি হেডলাইন নেওয়া (আপনি চাইলে সংখ্যা বাড়াতে পারেন)
    for entry in feed.entries[:5]:
        news_content += f"* [{entry.title}]({entry.link})\n"
    
    return news_content

def get_gold_price():
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
        
        price = data.get('price', 'N/A')
        price_gram_24k = data.get('price_gram_24k', 'N/A')
        
        # তারিখটি সুন্দরভাবে দেখানোর জন্য
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"## 💰 সোনার দামের আপডেট ({current_time})\n" \
               f"* **প্রতি আউন্স:** ${price} USD\n" \
               f"* **প্রতি গ্রাম (২৪ ক্যারেট):** ${price_gram_24k} USD\n"
    except Exception as e:
        return f"Error fetching price: {e}\n"

def write_to_file(price_data, news_data):
    # সব তথ্য একসাথে index.md ফাইলে জমা করা (যাতে সরাসরি সাইটে দেখা যায়)
    with open("index.md", "a", encoding="utf-8") as f:
        f.write(price_data + "\n")
        f.write(news_data + "\n")
        f.write("\n---\n")

if __name__ == "__main__":
    # দাম এবং খবর দুটোই সংগ্রহ করা
    price_info = get_gold_price()
    news_info = get_gold_news()
    
    # ফাইলে সেভ করা
    write_to_file(price_info, news_info)
