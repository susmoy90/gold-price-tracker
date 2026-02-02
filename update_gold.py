import requests
import feedparser
import os
import datetime

def get_bdt_rate():
    try:
        # লাইভ USD to BDT এক্সচেঞ্জ রেট
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data.get('rates', {}).get('BDT', 122.0)
    except:
        return 122.0

def get_gold_news():
    news_url = "https://news.google.com/rss/search?q=gold+price+market+bangladesh"
    feed = feedparser.parse(news_url)
    
    news_table = "### 📰 আজকের সর্বশেষ খবর (News Table)\n\n"
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
        
        # ২৪ ক্যারেট প্রতি গ্রামের লাইভ ডলার প্রাইস
        p24k_usd = gold_data.get('price_gram_24k', 0)
        usd_to_bdt = get_bdt_rate()
        p24k_bdt = p24k_usd * usd_to_bdt
        
        # ১ ভরি = ১১.৬৬৪ গ্রাম
        v_gm = 11.664 

        def f_bdt(val):
            return "{:,.2f}".format(val)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"# 💰 সোনার দামের লাইভ আপডেট (বাংলাদেশ পাইকারি বাজার)\n"
        output += f"**শেষ আপডেট:** {current_time}\n\n"
        output += f"### ✨ আজকের ১ গ্রাম ২৪ ক্যারেট সোনার দাম: **{f_bdt(p24k_bdt)} ৳**\n"
        output += f"*(১$ = {usd_to_bdt} BDT হিসেবে)*\n\n"
        output += f"> **হিসাব:** ১ ভরি = {v_gm} গ্রাম | আন্তর্জাতিক মান অনুযায়ী পাইকারি রেট\n\n"

        # টেবিল ১: প্রতি গ্রামের দাম
        output += "### ⚖️ প্রতি গ্রামের দাম (Gram Price)\n\n"
        output += "| ক্যারেট | বিশুদ্ধতা (Ratio) | দাম (BDT) | দাম (USD) |\n"
        output += "| :--- | :--- | :--- | :--- |\n"
        
        # টেবিল ২: প্রতি ভরির দাম
        v_table = "\n### 🔱 প্রতি ভরির দাম (Vhori Price)\n\n"
        v_table += "| ক্যারেট | বিশুদ্ধতা (Ratio) | দাম (BDT) | দাম (USD) |\n"
        v_table += "| :--- | :--- | :--- | :--- |\n"

        # আপনার দেওয়া পাইকারি বাজারের রেশিও চার্ট
        # 24K=1.0, 22K=22/24, 21K=21/24, 18K=18/24, Old=0.75
        for name, ratio in [("24K", 1.0), ("22K", 22/24), ("21K", 21/24), ("18K", 18/24), ("Old Gold", 0.75)]:
            u_gm = p24k_usd * ratio
            b_gm = u_gm * usd_to_bdt
            
            # গ্রাম টেবিল আপডেট
            output += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(b_gm)} ৳ | ${round(u_gm, 2)} |\n"
            
            # ভরি টেবিল আপডেট
            v_table += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(b_gm * v_gm)} ৳ | ${round(u_gm * v_gm, 2)} |\n"
        
        return output + v_table + "\n"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price() + get_gold_news())
