import requests
import json
import os
from datetime import datetime

def fetch_matches():
    today = datetime.now().strftime('%Y-%m-%d')
    # نحاول جلب مباريات اليوم بالكامل
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {"x-apisports-key": os.getenv("RAPIDAPI_KEY")}
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            fixtures = data.get('response', [])
            
            if not fixtures:
                print("الـ API لم يرجع أي مباريات اليوم.")
                return []

            matches = []
            for item in fixtures:
                status_short = item['fixture']['status']['short']
                m_time = item['fixture']['date'][11:16]
                
                # ترجمة الحالة للعربية
                arabic_status = "لم تبدأ"
                if status_short == "FT": arabic_status = "انتهت"
                elif status_short in ["1H", "2H", "HT", "P", "LIVE"]: arabic_status = "مباشر"

                matches.append({
                    "team1": item['teams']['home']['name'],
                    "team1_logo": item['teams']['home']['logo'],
                    "team2": item['teams']['away']['name'],
                    "team2_logo": item['teams']['away']['logo'],
                    "team1_score": str(item['goals']['home'] if item['goals']['home'] is not None else 0),
                    "team2_score": str(item['goals']['away'] if item['goals']['away'] is not None else 0),
                    "minute": str(item['fixture']['status']['elapsed'] if item['fixture']['status']['elapsed'] else 0),
                    "status": "LIVE" if arabic_status == "مباشر" else status_short,
                    "status_ar": arabic_status,
                    "league": item['league']['name'],
                    "match_time": m_time,
                    "date_time": item['fixture']['date'][:-6],
                    "channel": "beIN Sports",
                    "commentator": "جاري التحديد"
                })
            return matches[:50] # جلب أول 50 مباراة
    except Exception as e:
        print(f"حدث خطأ أثناء الجلب: {e}")
    return []

def main():
    print("بدء عملية التحديث...")
    all_matches = fetch_matches()
    
    # تحميل القنوات الحالية للحفاظ عليها
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                if content:
                    full_data = json.loads(content)
            except:
                print("فشل في قراءة api.json القديم، سيتم إنشاء واحد جديد.")

    # إذا كانت القائمة فارغة، سنضيف مباراة تجريبية واحدة لنتأكد أن الملف يعمل
    if not all_matches:
        print("تنبيه: القائمة فارغة، سيتم إضافة مباراة وهمية للتجربة.")
        all_matches = [{
            "team1": "فريق تجريبي",
            "team1_logo": "",
            "team2": "خصم تجريبي",
            "team2_logo": "",
            "team1_score": "0",
            "team2_score": "0",
            "minute": "0",
            "status": "NS",
            "status_ar": "قريباً",
            "league": "دوري تجريبي",
            "match_time": "00:00",
            "date_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "channel": "قناة الاختبار",
            "commentator": "معلق الاختبار"
        }]

    full_data['live_matches'] = all_matches
    
    # كتابة البيانات وحفظها
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)
    print(f"تم بنجاح تحديث {len(all_matches)} مباراة.")

if __name__ == "__main__":
    main()
