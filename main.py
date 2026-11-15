import requests

def check_stocks():
    print("--- 📊 گزارش لحظه‌ای بازار بورس ---")
    
    # سهم‌هایی که می‌خواهیم چک کنیم (فولاد و خودرو)
    symbols = ["فولاد", "خودرو"]
    
    # آدرس API برای دریافت اطلاعات بازار
    url = "https://api.tgju.org/v1/market/indicator/summary-table-data/stock"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            # جستجو در بین داده‌ها برای پیدا کردن سهم‌ها
            found_any = False
            for item in data.get('data', []):
                if len(item) > 1 and item[1] in symbols:
                    found_any = True
                    name = item[1]
                    price = item[2]
                    change = item[3]
                    print(f"🔹 سهم {name}: قیمت {price} - تغییر: {change}%")
            
            if not found_any:
                print("⚠️ سهم‌های مورد نظر در لیست امروز پیدا نشدند.")
                
        else:
            print(f"⚠️ خطا در اتصال به سایت. کد خطا: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    check_stocks()