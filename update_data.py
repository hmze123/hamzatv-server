import requests
import json
import os
from datetime import datetime

def fetch_matches():
    # جلب تاريخ اليوم بتنسيق YYYY-MM-DD
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"https://v3.football.api-sports.io/fixtures?date={today}"
    headers = {"x-apisports-key": os.getenv("RAPIDAPI_KEY")}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = []
            for item in data.get('response', []):
                # سنأخذ أهم 20 مباراة فقط لكي لا يثقل الملف
                matches.append({
                    "team1": item['teams']['home']['name'],
                    "team1_logo": item['teams']['home']['logo'],
                    "team2": item['teams']['away']['name'],
                    "team2_logo": item['teams']['away']['logo'],
                    "team1_score": item['goals']['home'] if item['goals']['home'] is not None else 0,
                    "team2_score": item['goals']['away'] if item['goals']['away'] is not None else 0,
                    "minute": item['fixture']['status']['elapsed'] if item['fixture']['status']['elapsed'] else 0,
                    "status": item['fixture']['status']['short'], # سيظهر حالة المباراة (NS, FT, LIVE)
                    "league": item['league']['name'],
                    "stream_url": "" # يمكنك إضافة روابط بث هنا لاحقاً
                })
            return matches[:25] # عرض أول 25 مباراة مهمة
    except Exception as e:
        print(f"Error: {e}")
        return []
    return []

def main():
    all_matches = fetch_matches()
    
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                full_data = json.load(f)
            except: pass

    # تحديث المباريات مع الحفاظ على القنوات
    full_data['live_matches'] = all_matches
    
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
