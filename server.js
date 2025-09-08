const express = require('express');
const app = express();
const port = 3000;

app.get('/api/data', (req, res) => {
  res.json({
    "categories": [
  {
    "categoryName": "الأخبار",
    "channels": [
      {
        "name": "Al Jazeera English",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Aljazeera_eng.svg/512px-Aljazeera_eng.svg.png",
        "streamUrl": "https://live-hls-web-aje.getaj.net/AJE/01.m3u8"
      },
      {
        "name": "France 24 English",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/France_24_logo.svg/512px-France_24_logo.svg.png",
        "streamUrl": "https://f24hls-i.akamaihd.net/hls/live/2000343/F24_EN_LO_HLS/master.m3u8"
      }
    ]
  },
  {
    "categoryName": "محتوى حر",
    "channels": [
      {
        "name": "Big Buck Bunny",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/512px-Big_buck_bunny_poster_big.jpg",
        "streamUrl": "http://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8"
      }
    ]
  }

    ],
    // ✨✨✨ تم تحديث قسم المباريات هنا ✨✨✨
    "matches": [
      {
        "team1_name": "السعودية",
        "team1_flag_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Flag_of_Saudi_Arabia.svg/128px-Flag_of_Saudi_Arabia.svg.png",
        "team2_name": "العراق",
        "team2_flag_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Flag_of_Iraq.svg/128px-Flag_of_Iraq.svg.png",
        "match_time": "04:00 PM",
        "competition": "كأس الخليج للشباب تحت 20 سنة",
        "commentator": "راشد عبدالرحمن",
        "channel_name": "Dubai Sports 1",
        "stream_url": "https://live-hls-web-aje.getaj.net/AJE/01.m3u8"
      },
      {
        "team1_name": "عمان",
        "team1_flag_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Flag_of_Oman.svg/128px-Flag_of_Oman.svg.png",
        "team2_name": "اليمن",
        "team2_flag_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Flag_of_Yemen.svg/128px-Flag_of_Yemen.svg.png",
        "match_time": "06:00 PM",
        "competition": "كأس الخليج للشباب تحت 20 سنة",
        "commentator": "أحمد الشحي",
        "channel_name": "Dubai Sports 1",
        "stream_url": "https://f24hls-i.akamaihd.net/hls/live/2000343/F24_EN_LO_HLS/master.m3u8"
      }
    ]
  });
});

app.listen(port, () => {
  console.log(`الخادم يعمل الآن على الرابط http://localhost:${port}`);
});