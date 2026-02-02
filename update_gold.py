import requests
import feedparser
import os
import datetime

def get_bdt_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data.get('rates', {}).get('BDT', 122.5)
    except:
        return 122.5

def get_gold_news():
    news_url = "https://news.google.com/rss/search?q=gold+price+market+bangladesh"
    feed = feedparser.parse(news_url)
    
    # নিউজের টেবিল ডিজাইন
    news_section = "\n---\n### 📰 সোনার বাজারের সর্বশেষ খবর\n\n"
    news_section += "| ক্রমিক | সংবাদের শিরোনাম | নিউজ পেপার | লিংক |\n"
    news_section += "| :--- | :--- | :--- | :--- |\n"
    
    for i, entry in enumerate(feed.entries[:5], 1):
        # শিরোনাম এবং সোর্স আলাদা করা
        title_parts = entry.title.split(' - ')
        paper_name = title_parts[-1] if len(title_parts) > 1 else "নিউজ সোর্স"
        main_title = " - ".join(title_parts[:-1]) if len(title_parts) > 1 else entry.title
        news_section += f"| {i} | {main_title} | **{paper_name}** | [পড়ুন]({entry.link}) |\n"
    
    return news_section

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
        v_gm = 11.664

        def f_bdt(val):
            return "{:,.0f}".format(val)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # হেডার ডিজাইন (টেবিল ভাঙা রোধ করতে এখানে অতিরিক্ত \n ব্যবহার করা হয়েছে)
        output = f"""
<div align="center">
  <h1 style="color: #D4AF37;">💰 বাংলাদেশ গোল্ড হোলসেল মার্কেট আপডেট</h1>
  <p><b>সর্বশেষ আপডেট:</b> {current_time} | <b>ডলার রেট:</b> 1$ = {usd_to_bdt} BDT</p>
  <p style="font-size: 1.2em; color: #27ae60;"><b>আজকের ১ গ্রাম ২৪ ক্যারেট (পাকা সোনা): {f_bdt(p24k_bdt)} ৳</b></p>
  <hr style="border: 0.5px solid #D4AF37;">
</div>

### ⚖️ পাইকারি বাজারের দাম (Wholesale Price)

| ক্যারেট | বিশুদ্ধতা | প্রতি গ্রাম (BDT) | প্রতি ভরি (১১.৬৬৪ গ্রাম) |
| :--- | :---: | :---: | :---: |
"""
        
        retail_table = """
### 🛍️ লোকাল কাস্টমার খুচরা দাম (২০% প্রিমিয়ামসহ)

| ক্যারেট | প্রতি গ্রাম (BDT) | প্রতি ভরি (BDT) |
| :--- | :---: | :---: |
"""

        carats = [("২৪ ক্যারেট", 1.0), ("২২ ক্যারেট", 22/24), ("২১ ক্যারেট", 21/24), ("১৮ ক্যারেট", 18/24)]

        for name, ratio in carats:
            b_gm = p24k_usd * ratio * usd_to_bdt
            wholesale_vhori = b_gm * v_gm
            retail_vhori = wholesale_vhori * 1.20
            retail_gram = b_gm * 1.20
            
            output += f"| {name} | {round(ratio*100, 1)}% | {f_bdt(b_gm)} ৳ | {f_bdt(wholesale_vhori)} ৳ |\n"
            retail_table += f"| {name} | {f_bdt(retail_gram)} ৳ | **{f_bdt(retail_vhori)} ৳** |\n"
        
        return output + retail_table + get_gold_news() + "\n---\n> **⚠️ সতর্কবার্তা:** এটি আন্তর্জাতিক তথ্যের ওপর ভিত্তি করে তৈরি। স্থানীয় দোকানভেদে দাম আলাদা হতে পারে।"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price())
