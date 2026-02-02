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
    news_table = "### 📰 Ajker Sorvoses Khobor\n\n"
    news_table += "| Kromik | Songbad Shironam | Uthso o Link |\n"
    news_table += "| :--- | :--- | :--- |\n"
    for i, entry in enumerate(feed.entries[:5], 1):
        news_table += f"| {i} | {entry.title} | [Ekhane Click Korun]({entry.link}) |\n"
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
        v_gm = 11.664 

        def f_bdt(val):
            return "{:,.2f}".format(val)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        output = f"# 💰 Gold Price Live Update (Bangladesh)\n"
        output += f"**Last Update:** {current_time} | **Dollar Rate:** 1$ = {usd_to_bdt} BDT\n\n"
        output += f"### ✨ Ajker 1 Gram 24K Gold Price: **{f_bdt(p24k_bdt)} ৳**\n\n"

        # Table 1: Gram Price (Wholesale)
        output += "### ⚖️ Proti Gramer Dam (Wholesale Gram Price)\n\n"
        output += "| Carat | Purity | Dam (BDT) | Dam (USD) |\n"
        output += "| :--- | :--- | :--- | :--- |\n"
        
        # Table 2: Vhori Price (Wholesale)
        v_table = "\n### 🔱 Proti Vhorir Dam (Wholesale Vhori Price)\n\n"
        v_table += "| Carat | Purity | Dam (BDT) | Dam (USD) |\n"
        v_table += "| :--- | :--- | :--- | :--- |\n"

        # Table 3: Retail Price for Local Customers (20% Extra)
        retail_table = "\n### 🛍️ Local Customer Retail Price (With 20% Premium)\n\n"
        retail_table += "| Carat | Proti Gram (BDT) | Proti Vhori (BDT) |\n"
        retail_table += "| :--- | :--- | :--- |\n"

        # Carat list: 24K, 22K, 21K, 18K, Old Gold
        for name, ratio in [("24K", 1.0), ("22K", 22/24), ("21K", 21/24), ("18K", 18/24), ("Old Gold", 0.75)]:
            u_gm = p24k_usd * ratio
            b_gm = u_gm * usd_to_bdt
            wholesale_vhori = b_gm * v_gm
            
            # 20% Premium Calculation
            retail_gram = b_gm * 1.20
            retail_vhori = wholesale_vhori * 1.20
            
            # Update Wholesale Tables
            output += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(b_gm)} ৳ | ${round(u_gm, 2)} |\n"
            v_table += f"| **{name}** | {round(ratio*100, 2)}% | {f_bdt(wholesale_vhori)} ৳ | ${round(u_gm * v_gm, 2)} |\n"
            
            # Update Retail Table
            retail_table += f"| **{name}** | {f_bdt(retail_gram)} ৳ | **{f_bdt(retail_vhori)} ৳** |\n"
        
        return output + v_table + retail_table + "\n"
    except Exception as e:
        return f"Error: {e}\n"

def write_to_file(content):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    write_to_file(get_gold_price() + get_gold_news())
