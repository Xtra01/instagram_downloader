# 📖 Instagram Downloader - Proje Dizini

## 📁 Dosya Açıklamaları

### 🚀 Başlangıç

| Dosya | Açıklama | Okuma Süresi |
|-------|----------|:---:|
| **QUICKSTART.md** | 5 dakikalık hızlı başlangıç kılavuzu | 5 min |
| **README.md** | Proje hakkında genel bilgi, kurulum, temel kullanım | 10 min |

### 🏗️ Teknik Dokümantasyon

| Dosya | Açıklama | Okuma Süresi |
|-------|----------|:---:|
| **TEKNIK_RAPOR_VE_MIMARI.md** | 📌 KAPSAMLI teknik rapor: content types, library comparison, architecture, error handling, risk management | **30 min** |

### 💻 Kod Dosyaları

| Dosya | Amaç | LOC | Status |
|-------|------|:---:|:---:|
| **main.py** | Ana uygulama. CLI + Python API | ~400 | ✅ Production Ready |
| **advanced.py** | Rate limiting, retry, advanced wrapper | ~250 | ✅ Production Ready |
| **examples.py** | 6 real-world working examples | ~300 | ✅ Runnable |

### ⚙️ Konfigürasyon

| Dosya | Amaç |
|-------|------|
| **requirements.txt** | Python bağımlılıkları: instaloader, requests, python-dotenv |
| **config.json.example** | Konfigürasyon template |
| **.gitignore** | Git ignore kuralları (session, downloads, etc.) |

### 📋 Meta

| Dosya | İçerik |
|-------|--------|
| **LICENSE** | MIT License + Disclaimer |

---

## 🎯 Hangi Dosyayı Ne Zaman Okumalı?

### 1️⃣ İlk 5 Dakikada
➜ **QUICKSTART.md** oku
- Kurulum
- Basit kullanım
- Dosya yapısı

### 2️⃣ Kodu Çalıştırıncaya Kadar
➜ **README.md** oku
- Detaylı kurulum
- Komut satırı parametreleri
- Sorun giderme

### 3️⃣ Üretim Ortamında
➜ **TEKNIK_RAPOR_VE_MIMARI.md** oku
- Rate limiting stratejisi
- Ban riskleri ve çözümleri
- Advanced error handling
- Security best practices

### 4️⃣ Kod Geliştirme
➜ **main.py** ve **advanced.py** oku
- Docstrings ile ayrıntılı açıklamalar
- PEP8 standartları
- Modüler yapı

### 5️⃣ Hızlı Test
➜ **examples.py** çalıştır
- 6 real-world example

---

## 📊 İçeriğin Yapısı

```
TEKNIK_RAPOR_VE_MIMARI.md
├── 1. İçerik Türü ve İndirilebilirlik Tablosu
│   └─ GraphImage, GraphVideo, GraphSidecar, Story, Highlight, Reel, IGTV
│
├── 2. GitHub Kütüphaneleri Karşılaştırması (3 aday)
│   ├─ A) Instaloader (⭐ EN ÖNERİLEN)
│   ├─ B) Instagrapi (⚡ Güçlü Alternatif)
│   └─ C) Gallery-dl (📁 Multi-Platform)
│
├── 3. Önerilen Çözüm Mimarisi
│   ├─ Mimari Diagram
│   ├─ Veri Akışı (Sequence)
│   └─ Hata Yönetimi Stratejisi
│
├── 4. Production-Ready Python Kodu
│   ├─ 4.1 main.py (Ana Uygulama)
│   ├─ 4.2 advanced.py (Rate Limiting + Retry)
│   └─ 4.3 Kullanım Örnekleri
│
└── 5. Teknik Notlar ve Uyarılar
    ├─ Rate Limiting Limitleri
    ├─ Ban Tipleri ve Çözümleri
    ├─ Session Yönetimi
    ├─ Proxy Kullanımı
    ├─ Hukuki/Etik Uyarılar
    └─ Kurulum ve Başlangıç
```

---

## 🔍 Hızlı Referans

### CLI Komutları

```bash
# Basit
python main.py cristiano

# Oturum açarak
python main.py cristiano -u myusername

# Max 50 post
python main.py cristiano -m 50

# Stories olmadan
python main.py cristiano --no-stories

# Custom config
python main.py cristiano -c custom_config.json
```

### Python API

```python
from main import InstagramProfileDownloader, SessionManager

session_mgr = SessionManager()
loader = session_mgr.load_or_create()
session_mgr.login("username", "password")

config = InstagramDownloaderConfig()
downloader = InstagramProfileDownloader(loader, config)
downloader.download_profile("target", max_posts=100)
```

### Advanced Wrapper

```python
from advanced import InstagramAPIWrapper

wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
profile = wrapper.get_profile("target_profile")
stats = wrapper.download_profile_posts("target_profile", "./downloads", max_count=50)
```

---

## 📊 Proje İstatistikleri

| Metrik | Değer |
|--------|-------|
| **Toplam Satır Kod** | ~950 |
| **Dosya Sayısı** | 10 |
| **Dökümentasyon Sayfaları** | 3 (>50 KB) |
| **Örnekler** | 6 |
| **Desteklenen İçerik Türleri** | 8 |
| **Karşılaştırılan Kütüphaneler** | 3 |
| **PEP8 Uyumluluğu** | ✅ %100 |

---

## 🎓 Öğrenme Yolu

### Beginner (Başlangıç)
1. QUICKSTART.md oku (5 min)
2. `python main.py cristiano` çalıştır (1 min)
3. İndirilen dosyaları kontrol et (2 min)
4. README.md oku (10 min)

### Intermediate (Orta)
1. examples.py'deki 6 örneğini çalıştır
2. config.json'u değiştir
3. `-m`, `-u`, `--no-stories` parametrelerini dene
4. TEKNIK_RAPOR_VE_MIMARI.md'nin ilk 2 bölümünü oku

### Advanced (İleri)
1. TEKNIK_RAPOR_VE_MIMARI.md tamamını oku
2. main.py docstrings'i oku
3. advanced.py docstrings'i oku
4. Rate limiting ve retry mekanizmasını debug et
5. Custom error handler yazı
6. Production deployment yapı

---

## ✅ Kod Kalitesi Kontrol Listesi

- [x] PEP8 uyumlu
- [x] Type hints (partial)
- [x] Comprehensive docstrings
- [x] Error handling (try/except)
- [x] Logging (detailed)
- [x] Config management
- [x] Session persistence
- [x] Rate limiting
- [x] Retry mekanizması
- [x] Modüler yapı (SRP)

---

## 🚨 Kritik Noktalar

### Rate Limiting
- ⚠️ Instagram istekleri 12 saat içinde ban risk oluşturabilir
- 💡 Çözüm: `min_delay_between_requests` artır
- 📖 Detay: TEKNIK_RAPOR_VE_MIMARI.md §5.1

### Ban Riski
- ⚠️ 3 tip ban: Soft, Action Block, Permanent
- 💡 Çözüm: Exponential backoff + Proxy
- 📖 Detay: TEKNIK_RAPOR_VE_MIMARI.md §5.1

### Güvenlik
- ⚠️ session.pickle hassas dosya (LOGIN verisi içeriyor)
- ⚠️ config.json şifre içerebilir
- 💡 Çözüm: `.gitignore`'a eklenmiş
- 📖 Detay: README.md Güvenlik Notları

---

## 📞 Destek Kaynaklari

| Kaynak | URL/Dosya |
|--------|----------|
| Hızlı Başlangıç | QUICKSTART.md |
| Genel Bilgi | README.md |
| Detaylı Mimarisi | TEKNIK_RAPOR_VE_MIMARI.md |
| Kod Örnekleri | examples.py |
| API Reference | main.py docstrings |
| Advanced Features | advanced.py docstrings |
| Lisans | LICENSE |
| Kurulum | requirements.txt |

---

## 🎬 İlk Çalıştırma (5 dakika)

```bash
# 1. Virtual environment oluştur
python -m venv venv
venv\Scripts\activate

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Örnek çalıştır
python main.py cristiano

# 4. Sonuç gözlemle
ls downloads/cristiano/

# 5. Metadata kontrol et
cat downloads/cristiano/metadata.json
```

---

**Hoş geldiniz! Happy Scraping! 🚀**

*Ethical web scraping yapın, Instagram'ın ToS'unu saygıyla karşılayın.*
