import requests
import json
import os
from datetime import datetime

def fetch_matches():
    today = datetime.now().strftime('%Y-%m-%d')
    # جلب مباريات اليوم بالكامل من الـ API الرسمي
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {"x-apisports-key": os.getenv("RAPIDAPI_KEY")}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = []
            for item in data.get('response', []):
                status_short = item['fixture']['status']['short']
                
                # استخراج الوقت (مثال: 20:45)
                m_time = item['fixture']['date'][11:16]
                
                # ترجمة الحالة للعربية
                arabic_status = "لم تبدأ"
                if status_short == "FT": arabic_status = "انتهت"
                elif status_short in ["1H", "2H", "HT", "P"]: arabic_status = "مباشر"

                matches.append({
                    "team1": item['teams']['home']['name'],
                    "team1_logo": item['teams']['home']['logo'],
                    "team2": item['teams']['away']['name'],
                    "team2_logo": item['teams']['away']['logo'],
                    "team1_score": str(item['goals']['home'] if item['goals']['home'] is not None else 0),
                    "team2_score": str(item['goals']['away'] if item['goals']['away'] is not None else 0),
                    "minute": str(item['fixture']['status']['elapsed'] if item['fixture']['status']['elapsed'] else 0),
                    "status": status_short,
                    "status_ar": arabic_status,
                    "league": item['league']['name'],
                    "match_time": m_time,
                    "date_time": item['fixture']['date'][:-6], # تنسيق المنبه: 2024-04-18T20:30:00
                    "channel": "beIN Sports", # قيمة افتراضية
                    "commentator": "غير محدد"
                })
            # جلب أهم 40 مباراة
            return matches[:40]
    except: return []
    return []

def main():
    all_matches = fetch_matches()
    # الحفاظ على القنوات الموجودة أصلاً
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                if content: full_data = json.loads(content)
            except: pass

    full_data['live_matches'] = all_matches
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
