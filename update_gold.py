import requests
import feedparser
import os
import datetime

def get_bdt_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data.get('rates', {}).get('BDT', 122.0)
    except:
        return 122.0

def get_gold_news():
    news_url = "https://news.google.com/rss/search?q=gold+price+market+bangladesh"
    feed = feedparser.parse(news_url)
    news_table = "### 📰 আজকের সর্বশেষ খবর\n\n"
    news_table += "| ক্রমিক | সংবাদের শিরোনাম | উৎস ও লিংক |\n"
    news_table += "| :--- | :--- | :--- |\n"
    for i, entry in enumerate(feed.entries[:5], 1):
        news_table += f"| {i} | {entry.title} | [এখানে ক্লিক করুন]({entry.link}) |\n"
    return news_table

def get_gold_price():
    api_key = os.getenv("GOLD_API_KEY")
    url = "https://www.goldapi.io/api/XAU/USD"
    headers = {"x-access-token": api_key, "Content-Type": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        gold_data = response.json()
        
        p24k_usd = gold_data.get('price_gram_24k', 0)
        usd_to_bdt = get_bdt_rate()
        p24k_bdt = p24k_usd * usd_to_bdt
        v_gm = 11.664 # ১ ভরি = ১১.৬৬৪ গ্রাম

        def f_bdt(val):
            return "{:,.2f}".format(val)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"# 💰 সোনার দামের লাইভ আপডেট (বাংলাদেশ)\n"
        output += f"**শেষ আপডেট:** {current_time} | **ডলার রেট:** 1$ = {usd_to_bdt} BDT\n\n"
        output += f"### ✨ আজকের ১ গ্রাম ২৪ ক্যারেট সোনার দাম: **{f_bdt(p24k_bdt)} ৳**\n\n"

        # টেবিল ১: পাইকারি গ্রাম রেট
        output += "### ⚖️ পাইকারি প্রতি গ্রামের দাম (Wholesale Gram Price)\n\n"
        output += "| ক্যারেট | বিশুদ্ধতা | দাম (BDT) | দাম (USD) |\n"
        output += "| :--- | :--- | :--- | :--- |\n"
        
        # টেবিল ২: পাইকারি প্রতি ভরির দাম
        v_table = "\n### 🔱 পাইকারি প্রতি ভরির দাম (Wholesale Vhori Price)\n\n"
        v_table += "| ক্যারেট | বিশুদ্ধতা | দাম (BDT) | দাম (USD) |\n"
        v_table += "| :--- | :--- | :--- | :--- |\n"

        # টেবিল ৩: লোকাল কাস্টমার খুচরা দাম (২০% লাভসহ)
        retail_table = "\n### 🛍️ লোকাল কাস্টমার খুচরা দাম (২০% প্রিমিয়ামসহ)\n\n"
        retail_table += "| ক্যারেট | প্রতি গ্রাম (BDT) | প্রতি ভরি (BDT) |\n"
        retail_table += "| :--- | :--- | :--- |\n"

        # ক্যারেট লিস্ট
        for name, ratio in [("24K", 1.0), ("22K", 22/24), ("21K", 21/24), ("18K", 18/24), ("Old Gold", 0.75)]:
            u_gm = p24k_usd * ratio
            b_gm = u_gm * usd_to_bdt
            wholesale_vhori = b_gm * v_gm
            
            # ২০% প্রিমিয়াম ক্যালকুলেশন
            retail_gram = b_gm * 1.20
            retail_vhori = wholesale_vhori * 1.20
            
            # পাইকারি টেবিল ডাটা
            output += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(b_gm)} ৳ | ${round(u_gm, 2)} |\n"
            v_table += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(wholesale_vhori)} ৳ | ${round(u_gm * v_gm, 2)} |\n"
            
            # খুচরা টেবিল ডাটা (২০% যোগ করা হয়েছে)
            retail_table += f"| **{name}** | {f_bdt(retail_gram)} ৳ | **{f_bdt(retail_vhori)} ৳** |\n"
        
        return output + v_table + retail_table + "\n"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price() + get_gold_news())
