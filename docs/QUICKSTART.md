# Instagram Downloader - Hızlı Başlangıç Kılavuzu

## Projeye Genel Bakış

Bu proje, **Instagram herkese açık profillerdeki medya varlıklarını sistematik bir şekilde arşivlemek** için tasarlanmış production-ready bir Python uygulamasıdır.

### Dosya Yapısı

```
instagram_downloader/
├── main.py                          # Ana uygulama (core)
├── advanced.py                      # Rate limiting & retry mekanizması
├── examples.py                      # 6 adet working example
├── requirements.txt                 # Bağımlılıklar
├── config.json.example              # Konfigürasyon template
├── .gitignore                       # Git ignore kuralları
├── README.md                        # Genel dokumentasyon
├── LICENSE                          # MIT License
└── TEKNIK_RAPOR_VE_MIMARI.md       # **ÖNEMLİ: Detaylı teknik rapor**
```

---

## ⚡ 5 Dakikalık Başlangıç

### 1. Kurulum (1 dakika)

```bash
# Repository klonla
git clone <repo-url>
cd instagram_downloader

# Virtual environment oluştur
python -m venv venv
venv\Scripts\activate          # Windows
# ya da: source venv/bin/activate  # Linux/macOS

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 2. Basit İndirme (1 dakika)

```bash
# Herkese açık bir profili indir
python main.py cristiano

# Ya da: Max 20 post indir
python main.py cristiano -m 20
```

### 3. Oturum Açarak İndirme (1 dakika)

```bash
# 2FA veya özel ayarlar gerektiriyorsa
python main.py target_profile -u your_instagram_username
# Şifre sorulacak (gizli girilir)
```

### 4. Dosyaları Kontrol Et (2 dakika)

```
downloads/
└── cristiano/
    ├── photos/          # .jpg resimler
    ├── videos/          # .mp4 videolar
    ├── carousel/        # Çoklu medya albümleri
    ├── stories/         # (2FA sayesinde) Hikayeler
    ├── reels/           # Reel videolar
    ├── highlights/      # Story highlights
    └── metadata.json    # Tüm metadata
```

---

## 📊 Teknik Mimarisi

### Temel Bileşenler

```
[Input: Username]
    ↓
[Session Manager] ← Session cache
    ↓
[Profile Downloader] ← Config
    ├─> [Directory Structure]
    ├─> [Metadata Extractor]
    ├─> [Media Downloader]
    │   ├─> Rate Limiter (2s delay + jitter)
    │   └─> Retry Handler (exponential backoff)
    └─> [JSON Report]
    ↓
[Local Archive + Metadata]
```

### Rate Limiting Stratejisi

| Senario | Strateji |
|---------|----------|
| Normal İstek | 2 saniye bekleme + %0-10 jitter |
| Error (429) | Exponential backoff: 2^n saniye |
| Max 5 deneme | Son denemede exception fırlat |

---

## 🔧 Kullanım Şekilleri

### Şekil 1: CLI (Komut Satırı)

```bash
# Basit
python main.py cristiano

# Gelişmiş
python main.py cristiano -m 50 -u myusername --no-stories -c custom_config.json
```

### Şekil 2: Python Script

```python
from main import InstagramProfileDownloader, SessionManager
from advanced import InstagramAPIWrapper

# Session hazırla
session_mgr = SessionManager()
loader = session_mgr.load_or_create()
session_mgr.login("username", "password")

# Downloader kullan
downloader = InstagramProfileDownloader(loader, config)
downloader.download_profile("target_profile", max_posts=100)
```

### Şekil 3: Advanced (Error Handling)

```python
from advanced import InstagramAPIWrapper

wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
profile = wrapper.get_profile("target_profile")
stats = wrapper.download_profile_posts("target_profile", "./downloads", max_count=50)

print(f"İndirilen: {stats['total_downloaded']}")
print(f"Başarısız: {stats['total_failed']}")
```

---

## 📋 Kod Kalitesi ve Standartlar

### PEP8 Uyumluluğu ✅

```python
# ✅ Doğru
def download_posts(self, profile, base_dir, max_count=None):
    """Docstring ile açıklama."""
    for idx, post in enumerate(posts):
        try:
            # İşlem
        except Exception as e:
            logger.error(f"Hata: {e}")

# ❌ Yanlış
def dl_posts(p, d):
    for i,po in enumerate(p):
        pass  # Açıklama yok
```

### Modüler Yapı ✅

- `main.py`: Core functionality
- `advanced.py`: Advanced features (rate limiting, retry)
- `examples.py`: 6 real-world örnek
- Ayrı sorumluluk prensipleri (SRP)

### Hata Yönetimi ✅

```python
try:
    profile = downloader.get_profile("username")
except ProfileNotExistsException:
    logger.error("Profil bulunamadı")
except PrivateProfileNotFollowedException:
    logger.error("Profil özel")
except Exception as e:
    logger.error(f"Beklenmeyen hata: {e}")
```

---

## ⚠️ Önemli Uyarılar

### 1. Instagram Rate Limiting

```
Maksimum İstek (Saatlik):
- Profile GET: ~200
- Media GET: ~500
- Search: ~30

Eğer 429 hatası alırsanız:
→ 12-24 saat bekleyin
→ min_delay_between_requests artırın
```

### 2. Ban Riskleri

| Ban Tipi | Süre | Sebep | Çözüm |
|----------|------|-------|-------|
| Soft Ban | 6-48s | Çok hızlı istek | Delay artır |
| Action Block | 24-72s | Spam aktivite | Bekle, hiç istek gönderme |
| Permanent | ∞ | Tekrarlayan ihlal | İnsan müdahalesi |

### 3. Hukuki/Etik

❌ **YAPMA:**
- Private hesaplara erişme
- Ticari kullanım
- Veri satış
- Ek bir endüstriye lisans olmadan

✅ **YAPABILIRSIN:**
- Kişisel araştırma
- OSINT analizi
- Academic research
- Ticari lisans ile

---

## 🚀 Performance Tips

```python
# 1. Rate Limiting'i artır (daha güvenli)
config["min_delay_between_requests"] = 5  # Default: 2

# 2. Post limitini belirle
python main.py profile -m 50  # İlk 50 post

# 3. Stories deaktif (hızlı)
python main.py profile --no-stories

# 4. Advanced wrapper kullan (retry + exponential backoff)
wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
```

---

## 📚 Detaylı Referans

### Tüm Seçenekler

```bash
usage: main.py [-h] [-u LOGIN_USER] [-p PASSWORD] [-m MAX_POSTS] 
               [--no-stories] [-c CONFIG] username

positional arguments:
  username              İndirilecek Instagram profil adı

optional arguments:
  -h, --help            Yardım göster
  -u, --login-user      Instagram giriş kullanıcı adı
  -p, --password        Instagram şifresi
  -m, --max-posts       Maximum indirilecek post sayısı
  --no-stories          Stories indirmeyi devre dışı bırak
  -c, --config          Konfigürasyon dosyası yolu
```

### Config Dosyası

```json
{
    "base_download_dir": "downloads",      // İndirme klasörü
    "session_file": "session.pickle",      // Session cache
    "min_delay_between_requests": 2,       // Saniye cinsinden
    "max_retries": 3,                      // Retry sayısı
    "download_stories": true,              // Stories indir
    "download_highlights": true,           // Highlights indir
    "download_reels": true                 // Reels indir
}
```

---

## 🔍 İçerik Türleri ve Indirilebilirlik

| Türü | Indirilebilir | Açıklama |
|------|:---:|----------|
| **Statik Fotoğraf** | ✅ | GraphImage |
| **Video Paylaşım** | ✅ | GraphVideo |
| **Carousel (Album)** | ✅ | GraphSidecar |
| **Reel** | ✅ | GraphReel |
| **IGTV** | ✅ | IGTV variant |
| **Story** | ⚠️ | Yalnızca 24 saat |
| **Story Highlight** | ⚠️ | Public highlights |
| **Live Video** | ❌ | Canlı yayın |

---

## 🛠️ Sorun Giderme

### Sorun: "ProfileNotExistsException"

```python
# Çözüm:
# 1. Profil adını kontrol et (boşluk, typo)
# 2. Profil herkese açık mı kontrol et
# 3. Instagram'ın adı değiştirmiş olabileceğini kontrol et
```

### Sorun: "429 Too Many Requests"

```python
# Çözüm:
# 1. 12-24 saat bekle
# 2. min_delay_between_requests artır
# 3. VPN/Proxy kulla
# 4. rate limiter'ı debug et:

wrapper = InstagramAPIWrapper(loader, min_delay=5.0, max_retries=5)
```

### Sorun: "PrivateProfileNotFollowedException"

```python
# Çözüm:
# Bu araç sadece herkese açık profilleri destekler.
# Özel hesap sahibi tarafından takip edilmiyorsanız indirme yapılamaz.
```

### Sorun: Session Hatası

```bash
# Çözüm:
# 1. Session dosyasını sil
rm session.pickle

# 2. Yeniden login yap
python main.py username -u myusername
```

---

## 📖 Daha Fazla Bilgi

- **Detaylı Teknik Rapor:** `TEKNIK_RAPOR_VE_MIMARI.md` (çok detaylı)
- **Örnekler:** `examples.py` (6 working example)
- **API Reference:** `main.py` docstrings
- **Advanced Usage:** `advanced.py` docstrings

---

## 🤝 Katkıda Bulunma

```bash
# Fork yap
git fork

# Feature branch oluştur
git checkout -b feature/amazing-feature

# Commit yap
git commit -m "Add amazing feature"

# Push yap
git push origin feature/amazing-feature

# Pull Request aç
```

---

## 📄 Lisans ve Disclaimer

**MIT License** - Detaylar için `LICENSE` dosyasını okuyun.

⚠️ **DISCLAIMER:**
- Bu araç kişisel, ticari olmayan kullanım için tasarlanmıştır.
- Instagram'ın ToS'unu ihlal etmeyiniz.
- Telif hakkı yasalarına uyunuz.
- Yazarlar, yanlış kullanımdan sorumlu değildir.

---

## 📞 Destek

Sorular veya sorunlar için:
1. GitHub Issues açın
2. Belirtileri ve hata mesajlarını paylaşın
3. Çalıştığınız Python sürümünü belirtin

---

**Happy Scraping! 🚀**

*Ethical web scraping yapın, Instagram'ın ToS'unu saygıyla karşılayın.*
