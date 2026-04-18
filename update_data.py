import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_arabic_matches():
    # سنستخدم مصدر بيانات رياضي عربي (مثال للتعامل مع هيكل المواقع العربية)
    url = "https://www.filgoal.com/matches/" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    matches = []
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # البحث عن حاوية المباريات (هذا الهيكل يتغير حسب الموقع المصدر)
        match_containers = soup.select('.mc-list-container .match-container')
        
        for item in match_containers:
            try:
                team1 = item.select_one('.f').text.strip()
                team2 = item.select_one('.s').text.strip()
                score = item.select_one('.m').text.strip().replace('\n', '')
                status = item.select_one('.match-status').text.strip()
                time = item.select_one('.match-time').text.strip()
                league = item.find_previous('h6').text.strip() if item.find_previous('h6') else "دوري غير محدد"
                
                # استخراج القناة والمعلق (إذا توفرا)
                channel = "غير مدرجة"
                commentator = "غير محدد"
                details = item.select('.m-details span')
                if len(details) > 0: channel = details[0].text.strip()
                if len(details) > 1: commentator = details[1].text.strip()

                matches.append({
                    "team1": team1,
                    "team1_logo": "", # المواقع العربية أحياناً تصعب جلب اللوجو، سنضع لوجو افتراضي
                    "team2": team2,
                    "team2_logo": "",
                    "team1_score": score.split('-')[0] if '-' in score else "0",
                    "team2_score": score.split('-')[1] if '-' in score else "0",
                    "minute": "0",
                    "status": "LIVE" if "جارية" in status else "NS",
                    "status_ar": status,
                    "league": league,
                    "match_time": time,
                    "date_time": "2024-04-18T" + time + ":00", # تاريخ تقريبي للمنبه
                    "channel": channel,
                    "commentator": commentator,
                    "stream_url": ""
                })
            except: continue
        return matches[:40]
    except: return []

def main():
    arabic_matches = fetch_arabic_matches()
    
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try: full_data = json.load(f)
            except: pass

    full_data['live_matches'] = arabic_matches
    
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
