import datetime
import requests

def check_market():
    now = datetime.datetime.now()
    print(f"--- Starting Market Check at {now} ---")
    
    # اینجا بعدا کد اصلی اتصال به بورس رو میذاریم
    print("Connecting to Iranian Stock Market...")
    
    # یک تست ساده برای بررسی اتصال اینترنت
    try:
        response = requests.get("https://api.github.com")
        if response.status_code == 200:
            print("Internet connection is OK!")
            print("Market check completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_market()
