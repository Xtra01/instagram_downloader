# 📁 Proje Yapısı - Instagram Downloader

## 🚀 Projeyi Başlatma

```bash
python start_web.py
```

Web arayüzü: http://localhost:5000

---

## 📂 Dizin Yapısı

```
instagram_downloader/
│
├── start_web.py              # 🚀 BAŞLATMA DOSYASI - Web uygulamasını başlatır
│
├── core/                     # 💾 İndirme motoru
│   ├── __init__.py
│   └── downloader.py        # Instagram indirme mantığı (Instaloader kullanır)
│
├── src/                      # 🔐 Oturum yönetimi
│   ├── __init__.py
│   ├── main.py             # SessionManager, Instaloader konfigürasyonu
│   └── advanced.py         # İleri düzey özellikler
│
├── web/                      # 🌐 Flask web uygulaması
│   ├── app.py              # Flask API ve rotalar
│   ├── cleanup_manager.py  # Otomatik temizlik (ŞU AN DEVRE DIŞI)
│   ├── rate_limiter.py     # DDoS koruması
│   ├── templates/
│   │   └── index.html      # Web arayüzü (Tailwind CSS)
│   └── static/             # CSS, JS, resimler
│
├── config/                   # ⚙️ Konfigürasyon örnekleri
│   ├── config.json.example
│   └── profiles.txt.example
│
├── docs/                     # 📚 Dokümantasyon
│   ├── INDEX.md            # Dokümantasyon indeksi
│   ├── QUICKSTART.md       # Hızlı başlangıç kılavuzu
│   ├── WEB_INTERFACE_GUIDE.md
│   └── ...                 # Diğer teknik dokümantasyonlar
│
├── downloads/                # 📥 İndirilen medya dosyaları
│   └── [kullanıcı_adı]/
│       ├── posts/          # Gönderiler
│       ├── videos/         # Videolar
│       ├── selected_posts/ # Seçili gönderiler
│       └── profile_picture/
│
├── temp_zips/                # 🗜️ Geçici ZIP dosyaları (otomatik temizlenir)
│
├── archive/                  # 🗄️ Kullanılmayan eski dosyalar
│   ├── old_scripts/        # Eski CLI scriptleri
│   ├── old_tests/          # Eski test dosyaları
│   └── temp_fixes/         # Geçici düzeltme scriptleri
│
├── requirements.txt          # 📦 Python bağımlılıkları
├── README.md                # 📖 Ana README
└── LICENSE                  # ⚖️ Lisans bilgisi
```

---

## 🔧 Temel Dosyalar

### `start_web.py`
- **Amaç:** Web uygulamasını başlatır
- **Kullanım:** `python start_web.py`
- **Port:** 5000

### `core/downloader.py`
- **Amaç:** Instagram indirme mantığı
- **Özellikler:** 
  - Profil indirme
  - Seçili gönderi indirme
  - Medya sayımı
  - Önizleme

### `web/app.py`
- **Amaç:** Flask API ve web arayüzü
- **Endpointler:**
  - `/api/preview` - Önizleme
  - `/api/download/selected` - Seçili indirme
  - `/api/download/zip` - ZIP indirme
  - `/api/profiles/list` - İndirilen profiller

### `web/cleanup_manager.py`
- **Durum:** ⚠️ DEVRE DIŞI (data loss önleme için)
- **Özellik:** Otomatik dosya temizliği
- **Ayar:** max_age_hours = 8760 (365 gün)

### `web/rate_limiter.py`
- **Durum:** ✅ AKTİF
- **Limitler:**
  - 10 istek/dakika
  - 100 istek/saat
  - 500 istek/gün

---

## 📦 Bağımlılıklar

```bash
pip install -r requirements.txt
```

### Ana Kütüphaneler:
- **Flask** - Web framework
- **Instaloader** - Instagram scraper
- **Pillow** - Görüntü işleme

---

## 🗄️ Arşivlenen Dosyalar

### `archive/old_scripts/`
- `run_batch.py` - Eski batch indirme scripti
- `run_downloader.py` - Eski CLI wrapper
- `run_tests.py` - Eski test runner
- `login.py` - Eski login scripti
- `configure_production.py` - Eski kurulum scripti

### `archive/temp_fixes/`
- `fix_paths.py` - Unicode path düzeltme scripti
- `final_fix.py` - Gelişmiş path düzeltme
- `test_counts.py` - Manuel sayım testi
- `test_integration.py` - Entegrasyon testi

### `archive/old_tests/`
- Eski test dosyaları ve testler

---

## ⚠️ Önemli Notlar

1. **Unicode Path Sorunu:** 
   - Instaloader Windows'ta `﹨` (U+FE68) karakteri kullanarak yanlış path oluşturuyordu
   - Çözüm: `dirname_pattern="{target}"` eklendi (src/main.py L124)

2. **Cleanup Manager:**
   - Veri kaybını önlemek için devre dışı bırakıldı
   - 24 saatlik TTL çok agresifti
   - Şimdi: 365 gün (8760 saat)

3. **Path Normalizasyonu:**
   - Tüm download fonksiyonları `.resolve()` kullanır
   - Unicode path sorunlarını önler

4. **Frontend Auto-Refresh:**
   - DOMContentLoaded event listener eklendi
   - Sayfa yüklendiğinde otomatik yenilenir

---

## 🐛 Bilinen Sorunlar

1. **Instagram Rate Limiting:**
   - Login olmadan 403 Forbidden hataları normal
   - Çözüm: Login kullan (ama şu an devre dışı)

2. **Unicode Paths:**
   - Eski indirmeler yanlış path'lerde olabilir
   - Yeni indirmeler düzgün çalışıyor

---

## 📝 Gelişim Geçmişi

Detaylı değişiklikler için:
- [docs/CHANGELOG_DEC_15_2025.md](docs/CHANGELOG_DEC_15_2025.md)
- [docs/FINAL_SUMMARY.md](docs/FINAL_SUMMARY.md)
- [docs/TEKNIK_RAPOR_VE_MIMARI.md](docs/TEKNIK_RAPOR_VE_MIMARI.md)
