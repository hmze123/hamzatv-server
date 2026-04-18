import requests
import json
import os
from datetime import datetime

def fetch_matches():
    today = datetime.now().strftime('%Y-%m-%d')
    # سنستخدم مفتاح API-Sports مباشرة
    headers = {
        'x-apisports-key': os.getenv("RAPIDAPI_KEY")
    }
    
    # قائمة ببعض الدوريات الكبرى (الدوري الإنجليزي 39، الإسباني 140، الأبطال 2، إلخ)
    # سنطلب مباريات اليوم لكل هذه الدوريات
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        data = response.json()
        fixtures = data.get('response', [])
        
        if not fixtures:
            print("لا توجد مباريات حقيقية مسجلة لهذا اليوم في الـ API.")
            return []

        matches = []
        for item in fixtures:
            # فلترة: نأخذ فقط الدوريات المعروفة أو التي فيها حالة (NS أو LIVE أو FT)
            status_short = item['fixture']['status']['short']
            m_time = item['fixture']['date'][11:16]
            
            matches.append({
                "team1": item['teams']['home']['name'],
                "team1_logo": item['teams']['home']['logo'],
                "team2": item['teams']['away']['name'],
                "team2_logo": item['teams']['away']['logo'],
                "team1_score": str(item['goals']['home'] if item['goals']['home'] is not None else 0),
                "team2_score": str(item['goals']['away'] if item['goals']['away'] is not None else 0),
                "minute": str(item['fixture']['status']['elapsed'] if item['fixture']['status']['elapsed'] else 0),
                "status": "LIVE" if status_short in ["1H", "2H", "HT", "P"] else status_short,
                "league": item['league']['name'],
                "match_time": m_time,
                "date_time": item['fixture']['date'][:-6],
                "channel": "beIN Sports",
                "commentator": "جاري التحديد"
            })
        return matches[:50]
    except Exception as e:
        print(f"Error: {e}")
        return []

def main():
    all_matches = fetch_matches()
    
    # تحميل البيانات الحالية
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                full_data = json.load(f)
            except: pass

    # إذا جلب مباريات حقيقية، نضعها. إذا لم يجد (القائمة فارغة) سيبقى على التجريبية لتعرف أن السكريبت عمل.
    if all_matches:
        full_data['live_matches'] = all_matches
        print(f"تم تحديث {len(all_matches)} مباراة حقيقية.")
    else:
        # هذه المباراة تظهر لك الآن لتعرف أن السكريبت وصل للـ API لكن لم يجد مباريات
        full_data['live_matches'] = [{
            "team1": "لا توجد مباريات اليوم",
            "team1_logo": "",
            "team2": "حاول لاحقاً",
            "team2_logo": "",
            "team1_score": "0",
            "team2_score": "0",
            "minute": "0",
            "status": "NS",
            "league": "تنبيه",
            "match_time": "00:00",
            "date_time": datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            "channel": "-",
            "commentator": "-"
        }]

    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
