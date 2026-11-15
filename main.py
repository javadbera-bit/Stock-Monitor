# pip install yfinance-ir Alilnvest-Codal pandas
import yfinance_ir as yf
import alilnvest_codal as cp
import pandas as pd
import numpy as np

# ==========================================
# ۱. تنظیمات و پارامترهای غربالگری
# ==========================================
MIN_MARKET_CAP = 10000  # حداقل ارزش بازار (به میلیارد تومان)
MIN_VOLUME = 1000000     # حداقل حجم معاملات روزانه
MAX_PE = 15              # حداکثر P/E قابل قبول
MIN_ROE = 0.15           # حداقل بازده حقوق صاحبان سهام (۱۵٪)
TOP_N = 5                # تعداد سهم‌های برتر برای نمایش

def screen_stock(symbol):
    """تحلیل یک سهم بر اساس معیارهای بنیادی و تکنیکال"""
    try:
        # --- بخش ۱: داده‌های قیمتی و تکنیکال (TSETMC) ---
        ticker = yf.Ticker(symbol)
        info = ticker.info
        hist = ticker.history(period="3mo") # داده‌های ۳ ماه اخیر
        
        if hist.empty:
            return None

        current_price = hist['Close'].iloc[-1]
        volume = hist['Volume'].iloc[-1]
        ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        
        # محاسبه نوسان (ریسک)
        volatility = hist['Close'].pct_change().std() * np.sqrt(252)

        # --- بخش ۲: داده‌های بنیادی (کدال) ---
        # دریافت صورت سود و زیان و ترازنامه
        income = cp.income_statement(symbol, max_reports=1)
        balance = cp.balance_sheet(symbol, max_reports=1)
        
        # استخراج مقادیر کلیدی (با مدیریت خطا در صورت نبود داده)
        try:
            net_income = income[0].get('net_income', 0)
            total_equity = balance[0].get('total_equity', 1)
            roe = net_income / total_equity if total_equity else 0
        except:
            roe = 0

        # --- بخش ۳: امتیازدهی و فیلترها ---
        score = 0
        reasons = []

        # فیلتر نقدشوندگی
        if volume > MIN_VOLUME:
            score += 1
            reasons.append("نقدشوندگی بالا")

        # فیلتر تکنیکال (روند صعودی)
        if current_price > ma_20 and ma_20 > ma_50:
            score += 2
            reasons.append("روند صعودی تکنیکال")

        # فیلتر بنیادی (سودآوری)
        if roe > MIN_ROE:
            score += 2
            reasons.append(f"ROE مناسب ({roe:.1%})")

        # فیلتر ریسک (نوسان کم)
        if volatility < 0.4:
            score += 1
            reasons.append("نوسان قابل قبول")

        return {
            'symbol': symbol,
            'price': current_price,
            'score': score,
            'reasons': reasons,
            'roe': roe,
            'pe': info.get('trailingPE', 'N/A'),
            'volatility': f"{volatility:.1%}"
        }
    except Exception as e:
        print(f"خطا در تحلیل {symbol}: {e}")
        return None

def run_market_screener():
    print("⏳ در حال دریافت لیست نمادهای بازار...")
    # دریافت لیست نمادها (برای سادگی، از یک لیست نمونه استفاده می‌کنیم. در واقعیت می‌توانید از API دیده‌بان استفاده کنید)
    symbols = ["فولاد", "فملی", "خودرو", "شپنا", "وبملت", "کگل", "فخوز", "شتران"]
    
    results = []
    for sym in symbols:
        print(f"🔍 در حال بررسی {sym}...")
        res = screen_stock(sym)
        if res and res['score'] >= 3: # فقط سهم‌هایی که حداقل امتیاز ۳ را دارند
            results.append(res)

    # مرتب‌سازی بر اساس امتیاز
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n" + "="*50)
    print(f"🏆 {TOP_N} سهم برتر بازار بر اساس تحلیل ترکیبی:")
    print("="*50)
    for i, r in enumerate(results[:TOP_N], 1):
        print(f"\n{i}. {r['symbol']} | قیمت: {r['price']:,.0f}")
        print(f"   🎯 امتیاز: {r['score']} | ROE: {r['roe']:.1%} | P/E: {r['pe']}")
        print(f"   📊 نوسان: {r['volatility']}")
        print(f"   ✅ دلایل: {', '.join(r['reasons'])}")

if __name__ == "__main__":
    run_market_screener()