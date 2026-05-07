import requests
import feedparser
import os
import datetime
import pytz

def get_bdt_rate():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        return data.get('rates', {}).get('BDT', 122.5)
    except:
        return 122.5

def get_api_usage(api_key):
    try:
        usage_url = "https://www.goldapi.io/api/usage"
        headers = {"x-access-token": api_key}
        response = requests.get(usage_url, headers=headers)
        data = response.json()
        requests_month = data.get('requests_month', 0)
        return f"\n> **📊 API Usage:** এই মাসে খরচ হয়েছে: `{requests_month}/100` টি রিকোয়েস্ট।"
    except:
        return ""

def fetch_news(query, count=5):
    url = f"https://news.google.com/rss/search?q={query}"
    feed = feedparser.parse(url)
    news_list = []
    for entry in feed.entries[:count]:
        title_parts = entry.title.split(' - ')
        paper_name = title_parts[-1] if len(title_parts) > 1 else "নিউজ সোর্স"
        main_title = " - ".join(title_parts[:-1]) if len(title_parts) > 1 else entry.title
        news_list.append({"title": main_title, "source": paper_name, "link": entry.link})
    return news_list

def get_combined_news():
    int_news = fetch_news("global+gold+market+price+update", 10)
    bd_news = fetch_news("gold+price+bangladesh+bajus+news", 5)
    
    section = "\n---\n### 🌏 আন্তর্জাতিক গোল্ড মার্কেট নিউজ (International - Top 10)\n\n"
    section += "| নং | আন্তর্জাতিক সংবাদ শিরোনাম | নিউজ পেপার | লিংক |\n"
    section += "| :--- | :--- | :--- | :--- |\n"
    for i, n in enumerate(int_news, 1):
        section += f"| {i} | {n['title']} | **{n['source']}** | [পড়ুন]({n['link']}) |\n"
        
    section += "\n### 🇧🇩 বাংলাদেশের গোল্ড মার্কেট নিউজ (Local)\n\n"
    section += "| নং | দেশীয় সংবাদ শিরোনাম | নিউজ পেপার | লিংক |\n"
    section += "| :--- | :--- | :--- | :--- |\n"
    for i, n in enumerate(bd_news, 1):
        section += f"| {i} | {n['title']} | **{n['source']}** | [পড়ুন]({n['link']}) |\n"
    return section

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

        p22k_usd, p21k_usd, p18k_usd = p24k_usd * (22/24), p24k_usd * (21/24), p24k_usd * (18/24)
        def f_bdt(val): return "{:,.0f}".format(val)
        
        current_time = datetime.datetime.now(pytz.timezone('Asia/Dhaka')).strftime("%Y-%m-%d %I:%M %p")

        output = f"""
<div align="center">
  <h1 style="color: #D4AF37;">💰 বাংলাদেশ গোল্ড হোলসেল মার্কেট আপডেট</h1>
  <p><b>সর্বশেষ আপডেট:</b> {current_time} | <b>ডলার রেট:</b> 1$ = {usd_to_bdt} BDT</p>
  <p style="font-size: 1.4em; color: #27ae60;"><b>আজকের ১ গ্রাম ২৪ ক্যারেট (পাকা সোনা): {f_bdt(p24k_bdt)} ৳</b></p>

  <table style="border-collapse: collapse; text-align: center; font-size: 1em; margin: 20px auto; border: 1px solid #ddd; min-width: 320px;">
    <tr style="background-color: #f8f9fa;">
      <th style="padding: 10px; border: 1px solid #ddd;">ক্যারেট</th>
      <th style="padding: 10px; border: 1px solid #ddd;">প্রতি গ্রাম ($)</th>
    </tr>
    <tr><td style="padding: 8px; border: 1px solid #ddd;">২৪ ক্যারেট</td><td style="padding: 8px; border: 1px solid #ddd;"><b>${p24k_usd:,.2f}</b></td></tr>
    <tr><td style="padding: 8px; border: 1px solid #ddd;">২২ ক্যারেট</td><td style="padding: 8px; border: 1px solid #ddd;"><b>${p22k_usd:,.2f}</b></td></tr>
    <tr><td style="padding: 8px; border: 1px solid #ddd;">২১ ক্যারেট</td><td style="padding: 8px; border: 1px solid #ddd;"><b>${p21k_usd:,.2f}</b></td></tr>
    <tr><td style="padding: 8px; border: 1px solid #ddd;">১৮ ক্যারেট</td><td style="padding: 8px; border: 1px solid #ddd;"><b>${p18k_usd:,.2f}</b></td></tr>
  </table>
  <hr style="border: 0.5px solid #D4AF37; width: 80%; margin: 20px auto;">
</div>

### ⚖️ পাইকারি বাজারের দাম (Wholesale Price)

| ক্যারেট | বিশুদ্ধতা | প্রতি গ্রাম (BDT) | প্রতি ভরি (১১.৬৬৪ গ্রাম) |
| :--- | :---: | :---: | :---: |
"""
        carats = [("২৪ ক্যারেট", 1.0), ("২২ ক্যারেট", 22/24), ("২১ ক্যারেট", 21/24), ("১৮ ক্যারেট", 18/24)]
        wholesale_rows = ""
        retail_rows = ""
        for name, ratio in carats:
            b_gm = p24k_usd * ratio * usd_to_bdt
            v_price = b_gm * v_gm
            wholesale_rows += f"| **{name}** | {round(ratio*100, 1)}% | {f_bdt(b_gm)} ৳ | {f_bdt(v_price)} ৳ |\n"
            retail_rows += f"| **{name}** | {f_bdt(b_gm*1.2)} ৳ | **{f_bdt(v_price*1.2)} ৳** |\n"
        
        retail_table_header = "\n### 🛍️ লোকাল কাস্টমার খুচরা দাম (২০% প্রিমিয়ামসহ)\n\n| ক্যারেট | প্রতি গ্রাম (BDT) | প্রতি ভরি (BDT) |\n| :--- | :---: | :---: |\n"
        
        usage_info = get_api_usage(api_key)
        return output + wholesale_rows + retail_table_header + retail_rows + get_combined_news() + "\n---\n" + usage_info + "\n\n> **⚠️ সতর্কবার্তা:** বাজার যাচাই করে লেনদেন করুন।"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price())
