# 📁 Instagram Downloader - Proje Klasör Yapısı

## Genel Bakış

Proje, modern Python standartlarına uygun, modüler ve okunabilir bir yapıda organize edilmiştir.

```
instagram_downloader/
│
├── 📂 src/                          # Kaynak Kod Klasörü
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # Ana uygulama (523 satır)
│   ├── advanced.py                  # İleri seviye özellikler (336 satır)
│   ├── examples.py                  # Kullanım örnekleri (259 satır)
│   └── batch_download.py            # Toplu indirme (350 satır)
│
├── 📂 tests/                        # Test Klasörü
│   ├── __init__.py                  # Test package initialization
│   └── test_basic.py                # Unit & integration testler (350 satır)
│
├── 📂 docs/                         # Dokümantasyon Klasörü
│   ├── TEKNIK_RAPOR_VE_MIMARI.md   # Detaylı teknik rapor
│   ├── PROJECT_COMPLETION.md        # Proje tamamlama özeti
│   ├── FINAL_SUMMARY.md             # Kapsamlı proje özeti
│   ├── QUICKSTART.md                # 5 dakikalık hızlı başlangıç
│   └── INDEX.md                     # Proje rehberi
│
├── 📂 config/                       # Konfigürasyon Klasörü
│   ├── config.json.example          # Örnek konfigürasyon dosyası
│   └── profiles.txt.example         # Örnek profil listesi
│
├── 📂 downloads/                    # İndirilen İçerik (Runtime)
│   └── {username}/                  # Her profil için klasör
│       ├── photos/                  # Fotoğraflar
│       ├── videos/                  # Videolar
│       ├── carousel/                # Carousel postlar
│       ├── stories/                 # Hikayeler
│       ├── reels/                   # Reels
│       ├── highlights/              # Highlight'lar
│       └── metadata.json            # Profil metadata
│
├── 🐍 run_downloader.py            # Ana script runner (wrapper)
├── 🐍 run_batch.py                 # Batch script runner (wrapper)
├── 🐍 run_tests.py                 # Test runner (wrapper)
│
├── 📄 README.md                     # Ana README (root)
├── 📄 requirements.txt              # Python bağımlılıkları
├── 📄 .gitignore                    # Git ignore kuralları
├── 📄 LICENSE                       # MIT License
│
└── 🗂️ Runtime Files (Git Ignore)
    ├── config.json                  # Aktif konfigürasyon
    ├── session.pickle               # Login session cache
    └── __pycache__/                 # Python cache

```

---

## 📂 Klasör Detayları

### 1. `src/` - Kaynak Kod Klasörü

**Amaç:** Tüm Python kaynak kodlarını organize bir şekilde saklar.

**İçerik:**
- `__init__.py`: Package tanımı, dışa aktarımlar
- `main.py`: Ana uygulama, CLI, profil indirme mantığı
- `advanced.py`: Rate limiting, exponential backoff, retry mekanizması
- `examples.py`: 6 farklı kullanım örneği
- `batch_download.py`: Toplu profil indirme özelliği

**Neden ayrı klasör?**
- Modülerlik ve temizlik
- Import path'lerinin açık olması
- Test edilebilirlik
- Package olarak dağıtılabilirlik

---

### 2. `tests/` - Test Klasörü

**Amaç:** Tüm test dosyalarını ayrı bir klasörde toplar.

**İçerik:**
- `__init__.py`: Test package tanımı
- `test_basic.py`: 15 unit test + integration test

**Test Coverage:**
- Config yönetimi testleri
- Rate limiter testleri
- Retry mekanizması testleri
- Session yönetimi testleri
- Downloader testleri
- Integration testleri

**Çalıştırma:**
```bash
python run_tests.py
# veya
pytest tests/test_basic.py -v
```

---

### 3. `docs/` - Dokümantasyon Klasörü

**Amaç:** Tüm dokümantasyonu tek bir yerde toplar.

**İçerik:**
- `TEKNIK_RAPOR_VE_MIMARI.md`: Mimari, API analizi, best practices
- `PROJECT_COMPLETION.md`: Proje tamamlama metrikleri
- `FINAL_SUMMARY.md`: Kapsamlı proje özeti
- `QUICKSTART.md`: 5 dakikalık başlangıç rehberi
- `INDEX.md`: Dosya navigasyon rehberi

**Kullanım:**
- Yeni geliştiriciler için onboarding
- API referansı
- Teknik kararların dokümantasyonu

---

### 4. `config/` - Konfigürasyon Klasörü

**Amaç:** Konfigürasyon şablonlarını saklar.

**İçerik:**
- `config.json.example`: Örnek konfigürasyon
- `profiles.txt.example`: Örnek profil listesi

**Kullanım:**
```bash
# Config kopyala ve özelleştir
cp config/config.json.example config.json

# Profil listesi oluştur
cp config/profiles.txt.example profiles.txt
nano profiles.txt
```

---

### 5. `downloads/` - İndirilen İçerik Klasörü

**Amaç:** Tüm indirilen içeriği organize eder.

**Yapı:**
```
downloads/
└── {username}/
    ├── photos/           # .jpg, .png dosyaları
    ├── videos/           # .mp4 dosyaları
    ├── carousel/         # Çoklu medya postları
    ├── stories/          # 24 saatlik hikayeler
    ├── reels/            # Kısa videolar
    ├── highlights/       # Kalıcı hikayeler
    └── metadata.json     # Profil bilgileri
```

**Not:** Bu klasör `.gitignore`'da olup Git'e eklenmez.

---

## 🐍 Runner Scripts (Root Dizini)

### `run_downloader.py`
Ana indirme script'ini çalıştırır.

```bash
python run_downloader.py cristiano -m 10
```

### `run_batch.py`
Toplu indirme script'ini çalıştırır.

```bash
python run_batch.py profiles.txt
```

### `run_tests.py`
Tüm testleri çalıştırır.

```bash
python run_tests.py
```

**Avantajları:**
- Root dizininden kolayca çalıştırma
- Import path sorunlarını çözer
- Kullanıcı dostu
- Örnek kullanım için referans

---

## 📄 Root Dosyalar

### `README.md`
Projenin ana dokümantasyonu. Hızlı başlangıç, kurulum, kullanım örnekleri.

### `requirements.txt`
Python bağımlılıkları:
```
instaloader>=4.14.0
requests>=2.31.0
python-dotenv>=1.0.0
```

### `.gitignore`
Git'e eklenmemesi gereken dosyalar:
- `session.pickle` (hassas)
- `config.json` (kullanıcıya özel)
- `downloads/` (büyük dosyalar)
- `__pycache__/` (cache)

### `LICENSE`
MIT License + etik kullanım uyarısı.

---

## 🔄 Dosya Akışları

### 1. Normal Kullanım Akışı
```
run_downloader.py
  └─> src/main.py
      ├─> src/advanced.py (rate limiting)
      ├─> config.json (konfigürasyon)
      ├─> session.pickle (login cache)
      └─> downloads/{username}/ (çıktı)
```

### 2. Batch Kullanım Akışı
```
run_batch.py
  └─> src/batch_download.py
      ├─> profiles.txt (input)
      └─> src/main.py (her profil için)
          └─> downloads/{username}/ (çıktı)
```

### 3. Test Akışı
```
run_tests.py
  └─> tests/test_basic.py
      ├─> src/main.py (import)
      └─> src/advanced.py (import)
```

---

## 📊 Klasör İstatistikleri

| Klasör | Dosya Sayısı | Toplam Satır | Boyut |
|--------|:---:|:---:|:---:|
| `src/` | 5 | ~1,820 | ~57 KB |
| `tests/` | 2 | ~350 | ~10 KB |
| `docs/` | 5 | ~1,470 | ~85 KB |
| `config/` | 2 | ~20 | ~1 KB |
| **Root** | 6 | ~150 | ~5 KB |
| **TOPLAM** | **20** | **~3,810** | **~158 KB** |

---

## 🎯 Tasarım Prensipleri

### 1. **Separation of Concerns**
- Kaynak kod, testler ve dokümantasyon ayrı
- Her klasörün tek sorumluluğu var

### 2. **Clean Architecture**
- Modüler yapı
- Bağımlılıklar açıkça tanımlı
- Test edilebilir kod

### 3. **User-Friendly**
- Root'tan kolayca çalıştırılabilir
- Açıklayıcı dosya isimleri
- README her klasörün amacını belirtir

### 4. **Maintainability**
- Kolay bulunabilir dosyalar
- Tutarlı isimlendirme
- Açık klasör hiyerarşisi

---

## 🚀 Yeni Geliştirici için Rehber

### 1. İlk Bakış (5 dakika)
```bash
# Proje yapısını incele
tree -L 2

# README'yi oku
cat README.md

# Hızlı test
python run_tests.py
```

### 2. Kod İncelemesi (15 dakika)
```bash
# Ana uygulama
cat src/main.py

# Test örnekleri
cat tests/test_basic.py

# Kullanım örnekleri
cat src/examples.py
```

### 3. İlk Kullanım (5 dakika)
```bash
# Konfigürasyon hazırla
cp config/config.json.example config.json

# Test çalıştır
python run_tests.py

# Örnek indir (gerçek API çağrısı yapmaz)
python run_downloader.py --help
```

---

## ✅ En İyi Uygulamalar

### Yeni Dosya Ekleme
- **Kaynak kod:** `src/` klasörüne ekle
- **Test:** `tests/` klasörüne ekle
- **Dokümantasyon:** `docs/` klasörüne ekle

### Import Path'ler
```python
# src/ içinden src/ dosyalarını import
from main import InstagramProfileDownloader
from advanced import RateLimiter

# tests/ içinden src/ dosyalarını import
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from main import InstagramProfileDownloader
```

### Git Commit
```bash
# Sadece kaynak kodu commit et
git add src/ tests/ docs/ *.py *.md requirements.txt

# Hassas dosyaları ignore et
# (zaten .gitignore'da)
```

---

## 📝 Özet

Bu klasör yapısı:
- ✅ **Modüler:** Her şey ayrı klasörlerde
- ✅ **Temiz:** İlk bakışta anlaşılır
- ✅ **Ölçeklenebilir:** Yeni özellikler kolayca eklenebilir
- ✅ **Profesyonel:** Endüstri standartlarına uygun
- ✅ **Test Edilebilir:** Testler ayrı klasörde
- ✅ **Dokümante:** Her şey açıkça belirtilmiş

**Başarılı bir Python projesi yapısı! 🎉**
