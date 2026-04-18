import requests
import json
import os
from datetime import datetime

def fetch_matches():
    # جلب تاريخ اليوم بتنسيق YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    # تعديل الرابط لجلب مباريات اليوم بالكامل وليس المباشر فقط
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {"x-apisports-key": os.getenv("RAPIDAPI_KEY")}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = []
            for item in data.get('response', []):
              matches.append({
    "team1": item['teams']['home']['name'],
    "team1_logo": item['teams']['home']['logo'],
    "team2": item['teams']['away']['name'],
    "team2_logo": item['teams']['away']['logo'],
    "team1_score": item['goals']['home'],
    "team2_score": item['goals']['away'],
    "minute": item['fixture']['status']['elapsed'],
    "status": item['fixture']['status']['short'],
    "league": item['league']['name'],
    "match_time": item['fixture']['date'][11:16], # الوقت فقط (20:30)
    "date_time": item['fixture']['date'][:-6],    # التاريخ الكامل للمنبه (2024-04-18T20:30:00)
    "stream_url": ""
})
            # جلب أهم 30 مباراة فقط لكي لا يكون التطبيق ثقيلاً
            return matches[:30]
    except Exception as e:
        print(f"Error: {e}")
        return []
    return []

def main():
    all_matches = fetch_matches()
    
    # قراءة القنوات الحالية للحفاظ عليها
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                full_data = json.load(f)
            except: pass

    # تحديث قسم المباريات
    full_data['live_matches'] = all_matches
    
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
