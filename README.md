# 🔮 Instagram Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/Xtra01/instagram_downloader?style=social)](https://github.com/Xtra01/instagram_downloader)

> **Modern, professional Instagram content downloader with web interface**

Instagram Downloader is a powerful Python application with a beautiful web interface for downloading public Instagram content. Download profiles, posts, reels, and IGTV videos with URL support, real-time progress tracking, and batch processing capabilities.

![Web Interface](docs/screenshot.png)

## ✨ Features

### 🌐 Web Interface
- **Modern UI** - Beautiful, responsive design with Tailwind CSS
- **Real-time Progress** - Live updates with detailed counters
- **URL Support** - Paste Instagram URLs directly
- **Batch Downloads** - Process multiple profiles at once
- **ZIP Downloads** - Download archived content easily

### 📥 Content Types
- ✅ **Profiles** - Download entire profiles with customizable limits
- ✅ **Posts** - Single post downloads via URL
- ✅ **Reels** - Download Instagram Reels videos
- ✅ **IGTV** - Long-form video support
- ✅ **Carousels** - Multi-image/video posts
- ✅ **Metadata** - Captions, likes, comments, timestamps

### 🔧 Technical Features
- 🚀 **Fast & Efficient** - Optimized download speeds
- 📊 **Progress Tracking** - Real-time progress with phase indicators
- 🔄 **Batch Processing** - Download multiple profiles simultaneously
- 💾 **Session Management** - Persistent sessions with retry logic
- 🎯 **Rate Limiting** - Intelligent throttling to avoid blocks
- 🔒 **Safe** - Respects Instagram's rate limits

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Xtra01/instagram_downloader.git
cd instagram_downloader

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Flask for web interface (optional)
pip install -r web/requirements.txt
```

### Launch Web Interface

```bash
python start_web.py
```

Open your browser: **http://localhost:5000**

## 📖 Usage

### 🌐 Web Interface (Recommended)

**Start the web server:**
```bash
python start_web.py
```

**Features:**
- 🎯 User-friendly interface
- 📊 Real-time progress tracking
- 👥 Batch downloads
- 🔗 URL support (profiles, posts, reels, IGTV)
- 📱 Mobile-responsive design
- 📁 Download management with ZIP export

**Examples:**

| Input | Type | Result |
|-------|------|--------|
| `cristiano` | Username | Downloads profile |
| `https://instagram.com/p/ABC123/` | Post URL | Downloads single post |
| `https://instagram.com/reel/XYZ789/` | Reel URL | Downloads reel |
| `https://instagram.com/tv/DEF456/` | IGTV URL | Downloads IGTV video |

**Detailed guide:** [QUICKSTART_URL_SUPPORT.md](QUICKSTART_URL_SUPPORT.md)

---

### 💻 Command Line Interface (CLI)

**Basic usage:**

```bash
# Download a public profile
python run_downloader.py cristiano

# Limit to 50 posts
python run_downloader.py cristiano -m 50

# Disable stories
python run_downloader.py cristiano --no-stories
```

**⚠️ Güvenlik Uyarısı:** Şifrenizi komut satırında yazmayın! Terminal geçmişinde kalır. Bunun yerine:

```bash
# Program şifre soracaktır (güvenli yöntem)
python run_downloader.py cristiano -u myusername

# Veya .env dosyası kullanın
cp .env.example .env
# .env dosyasını düzenleyin
```

### 📦 Toplu (Batch) İndirme

Birden fazla profili otomatik olarak indirmek için:

```bash
# Profil listesi dosyası oluştur
cp config/profiles.txt.example profiles.txt
# Düzenle: nano profiles.txt veya notepad profiles.txt

# Toplu indir
python run_batch.py profiles.txt

# Her profilden max 20 post, 10s delay
python run_batch.py profiles.txt -m 20 --delay 10
```

### Test Çalıştırma

```bash
# Tüm unit testleri çalıştır
python run_tests.py

# Pytest ile (opsiyonel)
pip install pytest
pytest tests/test_basic.py -v
```

### Alternatif Kullanım (Doğrudan)

```bash
# Doğrudan src klasöründen
cd src
python main.py cristiano

# Veya modül olarak
python -m src.main cristiano
```

### Tüm Seçenekler

```bash
# Ana downloader yardım
python run_downloader.py --help

# Batch downloader yardım
python run_batch.py --help
```

## Dosya Yapısı

```
instagram_downloader/
├── src/                         # Python kaynak kodları
│   ├── __init__.py
│   ├── main.py                  # Ana uygulama (523 satır)
│   ├── advanced.py              # İleri seviye özellikler (336 satır)
│   ├── examples.py              # Kullanım örnekleri (259 satır)
│   └── batch_download.py        # Toplu indirme (350 satır)
│
├── tests/                       # Test dosyaları
│   ├── __init__.py
│   └── test_basic.py            # Unit testler (350 satır)
│
├── docs/                        # Dokümantasyon
│   ├── README.md                # Bu dosyanın detaylı versiyonu
│   ├── QUICKSTART.md            # 5 dakikalık başlangıç
│   ├── INDEX.md                 # Proje rehberi
│   ├── TEKNIK_RAPOR_VE_MIMARI.md  # Detaylı teknik rapor
│   ├── PROJECT_COMPLETION.md    # Proje tamamlama özeti
│   └── FINAL_SUMMARY.md         # Kapsamlı proje özeti
│
├── config/                      # Konfigürasyon şablonları
│   ├── config.json.example      # Örnek konfigürasyon
│   └── profiles.txt.example     # Örnek profil listesi
│
├── downloads/                   # İndirilen içerik (runtime)
│   └── {username}/
│       ├── photos/
│       ├── videos/
│       ├── carousel/
│       ├── stories/
│       ├── reels/
│       ├── highlights/
│       └── metadata.json
│
├── run_downloader.py           # Ana script runner
├── run_batch.py                # Batch download runner
├── run_tests.py                # Test runner
├── requirements.txt            # Python bağımlılıkları
├── .gitignore                  # Git ignore kuralları
├── LICENSE                     # MIT License
└── README.md                   # Bu dosya
```

## Konfigürasyon

`config.json` dosyası otomatik olarak oluşturulur. İhtiyaç durumunda düzenleyebilirsiniz:

```json
{
    "base_download_dir": "downloads",
    "session_file": "session.pickle",
    "log_dir": "logs",
    "max_retries": 3,
    "request_timeout": 30,
    "min_delay_between_requests": 2,
    "download_stories": true,
    "download_highlights": true,
    "download_reels": true,
    "media_types": ["photo", "video", "carousel"]
}
```

## Teknik Mimarisi

Detaylı teknik mimarisi, API analizi ve best practices için `TEKNIK_RAPOR_VE_MIMARI.md` dosyasını okuyun.

### Rate Limiting

Uygulama, Instagram'ın istek sınırlarını göz önüne alan adaptive rate limiting mekanizması kullanır:

- Minimum bekleme: 2 saniye (varsayılan)
- Jitter (randomness): %0-10 varyasyon
- Exponential backoff: Hata durumunda 2^n stratejisi

### Hata Yönetimi

- **Soft Ban (429):** Otomatik exponential backoff
- **Profile Not Found (404):** Log ve pass
- **Private Profile:** Hata ve exit
- **Connection Error:** 3x retry
- **Invalid Session:** Yeniden login

## İleri Seviye Kullanım

### Python Script İçinde

```python
from main import InstagramProfileDownloader, SessionManager
from advanced import InstagramAPIWrapper

# Session oluştur
session_mgr = SessionManager()
loader = session_mgr.load_or_create()
session_mgr.login("username", "password")

# Advanced wrapper ile kullan
wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
profile = wrapper.get_profile("target_user")
stats = wrapper.download_profile_posts("target_user", "./downloads/target_user", max_count=100)

print(f"İndirilen: {stats['total_downloaded']}")
print(f"Başarısız: {stats['total_failed']}")
```

## Güvenlik Notları

⚠️ **ÖNEMLI:**

1. **Session Dosyası:** `session.pickle` hassas bilgi içerir. Paylaşmayın.
2. **Şifre:** CLI'de şifre girmek risklidir. Sorulursa gizli girilir.
3. **.gitignore:** `session.pickle` ve `config.json` otomatik ignore edilir.
4. **VPN/Proxy:** Çok sayıda profil indirirken proxy kullanımını düşünün.

## Yasal ve Etik Uyarılar

- ✅ **Herkese Açık Profiller:** Desteklenmektedir
- ❌ **Özel Profiller:** Hesaplama yapılmayan, yasal olmayan
- ❌ **Ticari Kullanım:** Instagram ToS ihlalidir
- ⚠️ **Veri Gizliliği:** İndirilen veriler GDPR kapsamında olabilir

## Sorun Giderme

### "ProfileNotExistsException" Hatası

```
Neden: Profil bulunamadı
Çözüm: Profil adını kontrol edin, herkese açık mı diye bakın
```

### "PrivateProfileNotFollowedException" Hatası

```
Neden: Profil özel
Çözüm: Sadece herkese açık profiller desteklenir
```

### "429 Too Many Requests" Hatası

```
Neden: Instagram istek sınırı aşıldı (Rate Limited)
Çözüm: 12-24 saat bekleyin, min_delay_between_requests artırın
```

### Session Hatası

```
Çözüm: session.pickle dosyasını silin ve yeniden login yapın
rm session.pickle
python main.py username -u myusername
```

## Performans İpuçları

1. **Rate Limiting:** `min_delay_between_requests` değerini artırın (default: 2s)
2. **Batch İşleme:** Bir seferde birkaç profil işleyin
3. **Post Limit:** `-m` flag'i ile maksimum post sayısını belirleyin
4. **Stories Deaktif:** `--no-stories` ile hikaye indirmeyi devre dışı bırakın

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART_URL_SUPPORT.md)** - Get started quickly with URL support
- **[Usage Limits & Guidelines](docs/USAGE_LIMITS_AND_GUIDELINES.md)** - Rate limits and best practices
- **[Web Deployment](docs/WEB_DEPLOYMENT.md)** - Deploy to production
- **[Web Interface Guide](docs/WEB_INTERFACE_GUIDE.md)** - UI/UX guide
- **[Changelog](docs/CHANGELOG_DEC_15_2025.md)** - Recent updates

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License
Copyright (c) 2025 Xtra01
```

## ⚠️ Disclaimer

**Legal Notice:**
- This tool is for **personal, educational, and non-commercial use only**
- Users must comply with Instagram's Terms of Service
- Only download **public profiles** - respect privacy
- Content creators retain all rights to their content
- We are not responsible for misuse of this tool

**Rate Limiting:**
- Instagram enforces rate limits (~200-500 requests/hour)
- Use reasonable limits (20-50 posts recommended)
- Add delays between batch downloads
- Respect the platform and content creators

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/Xtra01/instagram_downloader/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Xtra01/instagram_downloader/discussions)
- **Documentation:** Check the [docs](docs/) folder

## ⭐ Star History

If you find this project useful, please consider giving it a star! ⭐

## 🙏 Acknowledgments

- Built with [Instaloader](https://instaloader.github.io/)
- UI powered by [Tailwind CSS](https://tailwindcss.com/)
- Icons by [Font Awesome](https://fontawesome.com/)

---

**Made with ❤️ by [Xtra01](https://github.com/Xtra01)**

**Version:** 1.1.0 | **Last Updated:** December 15, 2025
