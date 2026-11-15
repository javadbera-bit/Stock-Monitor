import requests

def check_stocks():
    print("--- 🔍 تست اتصال به سایت ---")
    url = "https://api.tgju.org/v1/market/indicator/summary-table-data/stock"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=15)
        
        print(f"وضعیت پاسخ از سایت: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ داده‌ها دریافت شد. ۳ مورد اول را ببین:")
            # این بخش ۳ مورد اول دیتابیس رو چاپ میکنه تا ببینیم چه شکلیه
            for item in data.get('data', [])[:3]:
                print(item)
        else:
            print("⚠️ سایت به ما اجازه دسترسی نداد (احتمالا IP گیت‌هاب رو بلاک کرده).")
            
    except Exception as e:
        print(f"❌ خطای شبکه: {e}")

if __name__ == "__main__":
    check_stocks()