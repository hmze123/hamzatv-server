import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_arabic_matches():
    # استخدام مصدر يلا شوت لجلب مباريات اليوم
    url = "https://yalla-shoot.com/live/index.php"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    matches = []
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # البحث عن كتلة المباريات
        match_boxes = soup.find_all('div', class_='match-container')
        
        for box in match_boxes:
            try:
                # استخراج البيانات
                t1 = box.find('div', class_='team1').find('p').text.strip()
                t2 = box.find('div', class_='team2').find('p').text.strip()
                
                # الشعارات
                l1 = box.find('div', class_='team1').find('img')['src']
                l2 = box.find('div', class_='team2').find('img')['src']
                
                # النتيجة والوقت
                score = box.find('div', class_='result').text.strip()
                m_time = box.find('div', class_='match-time').text.strip()
                
                # القناة والمعلق
                chan = box.find('div', class_='channel').text.strip() if box.find('div', class_='channel') else "قناة غير معروفة"
                comm = box.find('div', class_='commentary').text.strip() if box.find('div', class_='commentary') else "غير محدد"
                
                # تحديد الحالة
                status = "NS"
                if ":" not in score and "-" in score: status = "LIVE"
                if "انتهت" in score: status = "FT"

                matches.append({
                    "team1": t1,
                    "team1_logo": l1,
                    "team2": t2,
                    "team2_logo": l2,
                    "team1_score": score.split('-')[0].strip() if '-' in score else "0",
                    "team2_score": score.split('-')[1].strip() if '-' in score else "0",
                    "minute": "0",
                    "status": status,
                    "league": "مباريات اليوم",
                    "match_time": m_time,
                    "date_time": datetime.now().strftime('%Y-%m-%d') + "T" + m_time + ":00",
                    "channel": chan,
                    "commentator": comm,
                    "stream_url": ""
                })
            except Exception as e:
                print(f"خطأ في مباراة معينة: {e}")
                continue
                
        return matches
    except Exception as e:
        print(f"فشل جلب الموقع: {e}")
        return []

def main():
    arabic_matches = fetch_arabic_matches()
    
    # قراءة القنوات الحالية للحفاظ عليها
    full_data = {"categories": [], "live_matches": []}
    if os.path.exists('api.json'):
        with open('api.json', 'r', encoding='utf-8') as f:
            try:
                content = f.read()
                if content:
                    full_data = json.loads(content)
            except: pass

    full_data['live_matches'] = arabic_matches
    
    # حفظ الملف
    with open('api.json', 'w', encoding='utf-8') as f:
        json.dump(full_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
