import requests
import json
import os

def fetch_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
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
                    "status": "LIVE",
                    "league": item['league']['name']
                })
            return matches
    except: return []
    return []

def main():
    live_matches = fetch_live_matches()
    
    # 1. محاولة قراءة البيانات الحالية (القنوات التي وضعتها أنت)
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                full_data = json.load(f)
            except: pass

    # 2. تحديث قسم المباريات فقط والحفاظ على الأقسام الأخرى
    full_data['live_matches'] = live_matches
    
    # 3. حفظ كل شيء معاً
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
