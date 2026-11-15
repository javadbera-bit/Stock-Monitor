import requests

def check_stocks():
    print("--- 📊 گزارش لحظه‌ای بازار بورس ---")
    
    symbols = ["فولاد", "خودرو"]
    
    # آدرس اصلی سایت بورس
    target_url = "https://api.tgju.org/v1/market/indicator/summary-table-data/stock"
    
    # استفاده از یک پروکسی قوی‌تر
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(proxy_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
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
            print(f"⚠️ خطا در اتصال به پروکسی. کد خطا: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    check_stocks()