import datetime
import requests

def check_market():
    now = datetime.datetime.now()
    print(f"--- Starting Market Check at {now} ---")
    
    # اتصال به یک API عمومی برای دریافت اطلاعات بازار
    url = "https://api.tgju.org/v1/market/indicator/summary-table-data/"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print("✅ Connection to the market is OK!")
            data = response.json()
            print("📊 Market data received successfully.")
            # در قدم‌های بعدی اینجا کد می‌نویسیم تا قیمت‌ها رو جدا کنه
        else:
            print(f"⚠️ Failed to connect. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error connecting: {e}")

if __name__ == "__main__":
    check_market()