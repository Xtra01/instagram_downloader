# 🚀 Instagram Downloader - Quick Start Guide

## ✨ Yeni Özellikler (15 Aralık 2025)

### 🎯 Artık URL İle İndirme!

**saveclip.app gibi siteler gibi, artık sadece username değil URL ile de indirebilirsiniz!**

---

## 📥 Desteklenen İçerik Türleri

### 1. **Profile İndirme** 👤
```
✅ Username: cristiano
✅ Profile URL: https://www.instagram.com/cristiano/
✅ Profile URL (short): instagram.com/cristiano
```

### 2. **Tekil Post İndirme** 📸
```
✅ Post URL: https://www.instagram.com/p/ABC123XYZ/
✅ Short Post URL: instagram.com/p/ABC123/
```

### 3. **Reel İndirme** 🎬
```
✅ Reel URL: https://www.instagram.com/reel/ABC123/
✅ Reels URL: https://www.instagram.com/reels/ABC123/
```

### 4. **IGTV İndirme** 📺
```
✅ IGTV URL: https://www.instagram.com/tv/ABC123/
```

### 5. **Story İndirme** 📖 (Yakında)
```
🔜 Story URL: https://www.instagram.com/stories/username/123456789/
```

---

## 🎯 Kullanım Örnekleri

### Örnek 1: Profil İndirme (Username)

**Input:**
```
cristiano
```

**Sonuç:**
- Profile'nin son 20-50 postu indirilir (limit belirtmediyseniz hepsi)
- Fotoğraflar ve videolar ayrı klasörlerde
- Metadata JSON dosyası

---

### Örnek 2: Profil İndirme (URL)

**Input:**
```
https://www.instagram.com/cristiano/
```

**Sonuç:**
- Username ile aynı
- URL'den otomatik username parse edilir

---

### Örnek 3: Tekil Post İndirme

**Input:**
```
https://www.instagram.com/p/C123ABC456/
```

**Sonuç:**
- Sadece o post indirilir (fotoğraf/video/carousel)
- Metadata (caption, likes, comments)
- Owner username klasörü oluşturulur

---

### Örnek 4: Reel İndirme

**Input:**
```
https://www.instagram.com/reel/C456DEF789/
```

**Sonuç:**
- Reel videosu indirilir
- Yüksek kalitede MP4
- Metadata ile birlikte

---

### Örnek 5: Batch İndirme (Karışık)

**Input:**
```
cristiano
https://www.instagram.com/instagram/
natgeo
https://www.instagram.com/p/ABC123/
barcelona
```

**Sonuç:**
- 3 profil (cristiano, instagram, natgeo, barcelona)
- 1 tekil post (ABC123)
- Her biri ayrı klasörde

---

## ⚙️ Maximum Posts Limiti

### Nasıl Çalışır?

**Önceki Problem:**
- Limit belirtsek bile tüm postlar indiriliyordu
- Progress bar hareket etmiyordu
- Kaç tane indiğini görmüyorduk

**Şimdi:**
- ✅ Limit tam olarak uygulanıyor
- ✅ Progress: "15 / 20" gösteriliyor
- ✅ Real-time güncelleme
- ✅ Limit gelince duruyor

---

### Kullanım:

#### Tek Profil:
```
Username: cristiano
Max Posts: 20
```
→ Tam 20 post indirilir, durur ✅

#### Batch:
```
Profiles:
- cristiano
- instagram
- natgeo

Max Posts: 10
```
→ Her profilden 10 post (toplam 30) ✅

---

## 📊 Progress Tracking

### Yeni Progress Göstergeleri:

**Initializing:**
```
[⏳] Initializing...
0 / 0
```

**Counting:**
```
[🧮] Counting items...
0 / 50 (estimated)
```

**Downloading:**
```
[⬇️] Downloading...
15 / 50 (30%)
15 completed · 0 failed · 35 remaining
```

**Completed:**
```
[✅] Completed
50 / 50 (100%)
50 completed · 0 failed · 0 remaining
```

---

## 🎨 Web Interface Kullanımı

### 1. Web Arayüzünü Aç
```
http://localhost:5000
```

### 2. Single Profile Tab

**Username veya URL gir:**
- `cristiano` (username)
- `https://instagram.com/p/ABC/` (post URL)
- `https://instagram.com/reel/XYZ/` (reel URL)

**Max Posts belirt (opsiyonel):**
- `20` → 20 post indir
- Boş → Hepsini indir

**Start Download tıkla!**

---

### 3. Progress İzle

**Active Downloads** bölümünde:
```
⏳ cristiano                              [Running]
████████████████████████░░░░ 75%
  ℹ️ Downloading...      15 / 20
  15 completed · 0 failed · 5 remaining
```

---

### 4. My Downloads

İndirme tamamlanınca:
```
✅ Download completed: cristiano - 20 items
```

**My Downloads** sekmesine git:
- İndirilen profiller listelenir
- "Download ZIP" ile indir
- Bilgisayarına kaydet

---

## 🔧 API Kullanımı (Developers)

### Single Download

**POST** `/api/download/single`

```json
{
  "username": "cristiano",
  "max_posts": 20
}
```

veya

```json
{
  "username": "https://www.instagram.com/p/ABC123/",
  "max_posts": null
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "uuid-here",
  "content_type": "post",
  "identifier": "ABC123",
  "message": "Post download started"
}
```

---

### Batch Download

**POST** `/api/download/batch`

```json
{
  "profiles": [
    "cristiano",
    "https://www.instagram.com/instagram/",
    "natgeo"
  ],
  "max_posts": 10
}
```

---

### Job Status

**GET** `/api/job/{job_id}`

**Response:**
```json
{
  "job_id": "uuid",
  "status": "running",
  "phase": "downloading",
  "progress": 75,
  "total_items": 20,
  "downloaded_items": 15,
  "failed_items": 0,
  "remaining_items": 5,
  "current_profile": "cristiano"
}
```

---

## ⚡ Performance Tips

### 1. **Optimal Limits**

| Kullanım | Önerilen Limit | Nedeni |
|----------|----------------|--------|
| Test | 5-10 posts | Hızlı test |
| Normal | 20-50 posts | Dengelidur |
| Archive | 100-200 posts | Tam arşiv |

### 2. **Batch Downloads**

- **Max 5-10 profil** per batch
- **10-20 post** per profile for batches
- **3-5 saniye** delay between profiles

### 3. **Rate Limiting**

Instagram limitleri:
- **200-500 requests/hour** (safe zone)
- **5 second** delay between batches
- **50-200 posts** per session

---

## 🚨 Troubleshooting

### Problem 1: Max Posts Çalışmıyor

**Belirti:**
- 20 limit koydun ama 50 indirdi

**Çözüm:**
- ✅ Artık düzeltildi!
- Backend manual iteration kullanıyor
- Limit tam olarak uygulanıyor

---

### Problem 2: Progress Bar Hareket Etmiyor

**Belirti:**
- İndirme başladı ama %0'da kaldı

**Çözüm:**
- ✅ Artık düzeltildi!
- Real-time progress tracking
- Her post sonrası güncelleme

---

### Problem 3: Kaç Tane İndiğini Görmüyorum

**Belirti:**
- "Initializing..." yazıyor sürekli

**Çözüm:**
- ✅ Artık düzeltildi!
- "15 / 20" gösteriliyor
- Phase indicators eklendi

---

### Problem 4: URL Kabul Etmiyor

**Belirti:**
- URL yapıştırdım ama hata verdi

**Çözüm:**
- ✅ Artık düzeltildi!
- Profile, Post, Reel, IGTV URL destekleniyor
- Otomatik parsing

---

## 📖 Kullanım Senaryoları

### Senaryo 1: Favori Sporcunun Profili

**Amaç:** Cristiano Ronaldo'nun son 50 postunu indir

**Adımlar:**
1. Input: `cristiano`
2. Max Posts: `50`
3. Start Download
4. Progress izle: 50/50 completed
5. My Downloads → Download ZIP

**Sonuç:** 50 post, ~200-500 MB

---

### Senaryo 2: Viral Reel İndir

**Amaç:** Bir reel URL'ini indir

**Adımlar:**
1. Instagram'da reel'i aç
2. "Copy Link" tıkla
3. URL'i web interface'e yapıştır
4. Start Download
5. 10-30 saniye içinde hazır!

**Sonuç:** Tek reel video, yüksek kalite

---

### Senaryo 3: Birden Fazla Profil

**Amaç:** 5 farklı profilden 20'şer post

**Adımlar:**
1. Batch Download tab'ı aç
2. Profilleri yaz:
   ```
   cristiano
   instagram
   natgeo
   barcelona
   realmadrid
   ```
3. Max Posts: `20`
4. Start Batch Download
5. İzle: 5 profil x 20 post = 100 post

**Sonuç:** 5 ayrı klasör, toplam ~500 MB-1 GB

---

## 🎓 Pro Tips

### Tip 1: URL'yi Instagram'dan Kopyala

**Instagram App:**
1. Post/Reel aç
2. (⋯) → "Copy Link"
3. Web interface'e yapıştır

**Instagram Web:**
1. Post'un URL'ini kopyala (address bar)
2. Web interface'e yapıştır

---

### Tip 2: Karışık Batch

Aynı anda hem username hem URL kullan:
```
cristiano
https://www.instagram.com/p/ABC123/
natgeo
https://www.instagram.com/reel/XYZ789/
barcelona
```

---

### Tip 3: Rate Limit'e Takılma

- Küçük limitler kullan (20-50)
- Batch'lerde 5-10 profil max
- Çok sık indirme yapma (1-2 saat ara)

---

## 📚 Daha Fazla Bilgi

- **Full Documentation:** [README.md](../README.md)
- **Rate Limits:** [USAGE_LIMITS_AND_GUIDELINES.md](./USAGE_LIMITS_AND_GUIDELINES.md)
- **Deployment:** [WEB_DEPLOYMENT.md](./WEB_DEPLOYMENT.md)
- **Technical Details:** [CHANGELOG_DEC_15_2025.md](./CHANGELOG_DEC_15_2025.md)

---

## 🎉 Özet

### Yeni Özellikler:
- ✅ URL ile indirme (Profile, Post, Reel, IGTV)
- ✅ Max posts limiti düzgün çalışıyor
- ✅ Real-time progress tracking
- ✅ Detaylı sayaçlar (15/20)
- ✅ Phase indicators (Initializing → Downloading → Completed)
- ✅ saveclip.app benzeri özellikler

### Desteklenen:
- ✅ Profile (username veya URL)
- ✅ Post (URL)
- ✅ Reel (URL)
- ✅ IGTV (URL)
- ✅ Batch (karışık)

### Düzeltilen Problemler:
- ✅ Max posts limiti uygulanıyor
- ✅ Progress bar güncelleniy or
- ✅ Item sayıları gösteriliyor
- ✅ URL parsing çalışıyor

---

**🚀 Kullanmaya Başla:** http://localhost:5000

**📞 Destek:** [README.md](../README.md) veya [USAGE_LIMITS_AND_GUIDELINES.md](./USAGE_LIMITS_AND_GUIDELINES.md)

---

**Last Updated:** December 15, 2025  
**Version:** 1.1.0  
**Status:** ✅ Production Ready with URL Support!
