import requests
import feedparser
import os
import datetime

def get_bdt_rate():
    # লাইভ কারেন্সি রেট (USD to BDT)
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data.get('rates', {}).get('BDT', 121.0) # ডিফল্ট ১২১ ধরবে
    except:
        return 121.0

def get_gold_news():
    # Google News থেকে গোল্ডের খবর
    news_url = "https://news.google.com/rss/search?q=gold+price+market+bangladesh"
    feed = feedparser.parse(news_url)
    news_content = "### 📰 আজকের সর্বশেষ খবর:\n"
    for entry in feed.entries[:5]:
        news_content += f"* [{entry.title}]({entry.link})\n"
    return news_content

def get_gold_price():
    api_key = os.getenv("GOLD_API_KEY")
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": api_key, "Content-Type": "application/json"}
    
    try:
        # গোল্ড প্রাইস ডেটা
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        gold_data = response.json()
        
        p24k_usd = gold_data.get('price_gram_24k', 0)
        usd_to_bdt = get_bdt_rate()
        
        # ক্যালকুলেশন লজিক
        def to_bdt(usd_val):
            return "{:,.2f}".format(usd_val * usd_to_bdt)

        p22k_usd = p24k_usd * (22/24)
        p18k_usd = p24k_usd * (18/24)
        old_gold_usd = p22k_usd * 0.90
        
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # টেবিল ও কন্টেন্ট তৈরি
        header = f"# 💰 সোনার দামের লাইভ আপডেট (বাংলাদেশ)\n"
        header += f"**শেষ আপডেট:** {current_time}\n\n"
        header += f"**আজকের ডলার রেট:** 1$ = {usd_to_bdt} BDT\n\n"
        
        table = "| ক্যারেট | প্রতি গ্রাম (BDT) | প্রতি গ্রাম (USD) |\n"
        table += "| :--- | :--- | :--- |\n"
        table += f"| **24K Gold** | {to_bdt(p24k_usd)} ৳ | ${round(p24k_usd, 2)} |\n"
        table += f"| **22K Gold** | {to_bdt(p22k_usd)} ৳ | ${round(p22k_usd, 2)} |\n"
        table += f"| **18K Gold** | {to_bdt(p18k_usd)} ৳ | ${round(p18k_usd, 2)} |\n"
        table += f"| **Old Gold** | {to_bdt(old_gold_usd)} ৳ | ${round(old_gold_usd, 2)} |\n\n"
        
        return header + table
    except Exception as e:
        return f"Error fetching price: {e}\n"

def write_to_file(content):
    # 'w' মোড ব্যবহার করায় আগের সব ডিলিট হয়ে শুধু নতুন তথ্য থাকবে
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    price_table = get_gold_price()
    news_info = get_gold_news()
    
    full_content = price_table + news_info
    write_to_file(full_content)
