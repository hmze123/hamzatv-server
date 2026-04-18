import requests
import json
import os

def fetch_live_matches():
    # رابط API-Sports المباشر
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        "x-apisports-key": os.getenv("RAPIDAPI_KEY")
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = []
            for item in data.get('response', []):
                match_info = {
                    "id": item['fixture']['id'],
                    "status": "LIVE",
                    "minute": item['fixture']['status']['elapsed'],
                    "team1": item['teams']['home']['name'],
                    "team1_logo": item['teams']['home']['logo'],
                    "team2": item['teams']['away']['name'],
                    "team2_logo": item['teams']['away']['logo'],
                    "team1_score": item['goals']['home'],
                    "team2_score": item['goals']['away'],
                    "league": item['league']['name']
                }
                matches.append(match_info)
            return matches
    except Exception as e:
        print(f"Error fetching matches: {e}")
    return []

def main():
    live_matches = fetch_live_matches()
    
    # محاولة فتح الملف، وإذا لم يوجد ننشئ هيكل جديد
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                full_data = json.load(f)
            except json.JSONDecodeError:
                full_data = {"categories": [], "live_matches": []}
    else:
        full_data = {"categories": [], "live_matches": []}

    # تحديث المباريات
    full_data['live_matches'] = live_matches
    
    # حفظ الملف (سيتم إنشاؤه تلقائياً إذا لم يكن موجوداً)
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully updated. Found {len(live_matches)} matches.")

if __name__ == "__main__":
    main()
