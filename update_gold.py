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
        
        # আপনার নতুন চাহিদামত ১ ভরি = ১১.৬৬৪ গ্রাম সেট করা হলো
        v_gm = 11.664 

        def f_bdt(val):
            return "{:,.2f}".format(val)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"# 💰 সোনার দামের লাইভ আপডেট (বাংলাদেশ)\n"
        output += f"**শেষ আপডেট:** {current_time}\n\n"
        output += f"### ✨ আজকের ১ গ্রাম ২৪ ক্যারেট সোনার দাম: **{f_bdt(p24k_bdt)} ৳**\n"
        output += f"*(১$ = {usd_to_bdt} BDT হিসেবে)*\n\n"
        output += f"> **হিসাব:** ১ ভরি = {v_gm} গ্রাম (Standard Bhori Measurement)\n\n"

        # টেবিল ১: গ্রাম
        output += "### ⚖️ প্রতি গ্রামের দাম (Gram Price)\n\n"
        output += "| ক্যারেট | দাম (BDT) | দাম (USD) |\n"
        output += "| :--- | :--- | :--- |\n"
        
        # টেবিল ২: ভরি
        v_table = "\n### 🔱 প্রতি ভরির দাম (Vhori Price)\n\n"
        v_table += "| ক্যারেট | দাম (BDT) | দাম (USD) |\n"
        v_table += "| :--- | :--- | :--- |\n"

        for k, ratio in [("24K", 1.0), ("22K", 22/24), ("18K", 18/24), ("Old", (22/24)*0.9)]:
            u_gm = p24k_usd * ratio
            b_gm = u_gm * usd_to_bdt
            output += f"| **{k} Gold** | {f_bdt(b_gm)} ৳ | ${round(u_gm, 2)} |\n"
            v_table += f"| **{k} Gold** | {f_bdt(b_gm * v_gm)} ৳ | ${round(u_gm * v_gm, 2)} |\n"
        
        return output + v_table + "\n"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price() + get_gold_news())
