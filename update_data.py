import requests
import json
import os

def fetch_live_matches():
    # رابط جلب المباريات المباشرة من API-Sports
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        "x-apisports-key": os.getenv("RAPIDAPI_KEY") # المفتاح الذي وضعته في Secrets
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            matches = []
            # استخراج أهم البيانات لتقليل حجم الملف
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
        print(f"Error: {e}")
    return []

def main():
    # 1. جلب المباريات المباشرة
    live_matches = fetch_live_matches()
    
    # 2. قراءة ملفك الحالي api.json
    try:
        with open('api.json', 'r', encoding='utf-8') as f:
            full_data = json.load(f)
    except:
        # إذا لم يكن الملف موجوداً، ننشئ بنية جديدة
        full_data = {"categories": [], "live_matches": []}

    # 3. تحديث قسم المباريات فقط
    full_data['live_matches'] = live_matches
    
    # 4. حفظ الملف المحدث
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)
    
    print(f"Done! Found {len(live_matches)} live matches.")

if __name__ == "__main__":
    main()
