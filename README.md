# 🔮 Instagram Downloader

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> **Modern Instagram content downloader with web interface**

Instagram Downloader is a powerful Python application with a beautiful web interface for downloading public Instagram content. Features real-time progress tracking, selective downloads, and ZIP export functionality.

---

## 🚀 Hızlı Başlangıç / Quick Start

### 1. Bağımlılıkları Yükle / Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Uygulamayı Başlat / Start Application

```bash
python start_web.py
```

### 3. Tarayıcıda Aç / Open in Browser

```
http://localhost:5000
```

---

## ✨ Özellikler / Features

### 🌐 Web Arayüzü / Web Interface
- **Modern UI** - Tailwind CSS ile responsive tasarım
- **Önizleme** - İndirmeden önce gönderi önizlemesi
- **Seçmeli İndirme** - İstediğiniz gönderileri seçin
- **ZIP İndirme** - Tüm içeriği tek ZIP dosyasında indirin
- **Canlı İlerleme** - Real-time progress tracking
- **Otomatik Yenileme** - Auto-refresh downloaded profiles

### 📥 İçerik Tipleri / Content Types
- ✅ **Fotoğraflar** - Single photos
- ✅ **Carousel** - Multiple photos/videos
- ✅ **Videolar** - Videos and Reels
- ✅ **Profil Resmi** - Profile pictures
- ✅ **Metadata** - Captions and timestamps

### 🔧 Teknik Özellikler / Technical Features
- 🚀 **Hızlı** - Optimized download speeds
- 📊 **İlerleme Takibi** - Detailed progress indicators
- 💾 **Oturum Yönetimi** - Session persistence
- 🎯 **Rate Limiting** - DDoS protection (10/min, 100/hr, 500/day)
- 🔒 **Güvenli** - Respects Instagram's rate limits

---

## 📁 Proje Yapısı / Project Structure

Detaylı proje yapısı için: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

```
instagram_downloader/
├── start_web.py          # 🚀 Ana başlatma dosyası / Main entry point
├── core/                 # 💾 İndirme motoru / Download engine
├── src/                  # 🔐 Oturum yönetimi / Session management
├── web/                  # 🌐 Flask web uygulaması / Flask app
├── config/               # ⚙️ Konfigürasyon / Configuration
├── docs/                 # 📚 Dokümantasyon / Documentation
├── downloads/            # 📥 İndirilen dosyalar / Downloaded files
└── archive/              # 🗄️ Eski dosyalar / Archived files
```

---

## 📚 Dokümantasyon / Documentation

- **[Proje Yapısı / Project Structure](PROJECT_STRUCTURE.md)** - Detaylı klasör yapısı
- **[Hızlı Başlangıç / Quick Start](docs/QUICKSTART.md)** - Başlangıç rehberi
- **[Web Arayüzü Kılavuzu / Web Interface Guide](docs/WEB_INTERFACE_GUIDE.md)** - UI kullanımı
- **[Teknik Rapor / Technical Report](docs/TEKNIK_RAPOR_VE_MIMARI.md)** - Mimari ve teknik detaylar
- **[Changelog](docs/CHANGELOG_DEC_15_2025.md)** - Güncellemeler

---

## 🔧 Gereksinimler / Requirements

- Python 3.8+
- Flask 2.x
- Instaloader 4.14.0+

---

## 📦 Kurulum / Installation

### Adım 1: Depoyu Klonla / Clone Repository

```bash
git clone https://github.com/Xtra01/instagram_downloader.git
cd instagram_downloader
```

### Adım 2: Virtual Environment Oluştur / Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

### Adım 3: Bağımlılıkları Yükle / Install Dependencies

```bash
pip install -r requirements.txt
```

### Adım 4: Uygulamayı Başlat / Launch Application

```bash
python start_web.py
```

**Tarayıcıda aç / Open in browser:** http://localhost:5000

---

## 🎯 Kullanım / Usage

### Web Arayüzü / Web Interface

1. **Kullanıcı adı gir** - Instagram kullanıcı adını yaz
2. **Önizleme göster** - "Show Preview" butonuna tıkla
3. **Gönderileri seç** - İstediğin gönderileri seç
4. **İndir** - "Download Selected" butonuna tıkla
5. **ZIP indir** - İndirme tamamlandıktan sonra "Download ZIP" ile toplu indir

### Desteklenen Formatlar / Supported Formats

| Girdi / Input | Tip / Type | Sonuç / Result |
|---------------|------------|----------------|
| `cristiano` | Kullanıcı adı | Profil indirilir |
| Fotoğraf seçimi | Seçmeli | Seçilen fotoğraflar |
| Video seçimi | Seçmeli | Seçilen videolar |
| Carousel | Çoklu medya | Tüm medya indirilir |

---

## ⚙️ Konfigürasyon / Configuration

### Rate Limiting

```python
# web/rate_limiter.py
RATE_LIMITS = {
    'per_minute': 10,
    'per_hour': 100,
    'per_day': 500
}
```

### Storage Cleanup (Disabled)

```python
# web/cleanup_manager.py
max_age_hours = 8760  # 365 days (currently disabled)
```

---

## 🐛 Sorun Giderme / Troubleshooting

### "403 Forbidden" Hatası
- **Sebep:** Instagram rate limiting
- **Çözüm:** Login kullanın veya bekleyin

### İndirilen dosyalar görünmüyor
- **Sebep:** Sayfa yenilenmedi
- **Çözüm:** Sayfa otomatik yenilenir, F5 ile manuel yenileyin

### ZIP indirme çalışmıyor
- **Sebep:** İndirme henüz tamamlanmadı
- **Çözüm:** "Active Downloads" %100 olana kadar bekleyin

---

## 🤝 Katkıda Bulunma / Contributing

Pull request'ler hoş karşılanır! Büyük değişiklikler için önce issue açın.

---

## ⚖️ Lisans / License

MIT License - Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 📧 İletişim / Contact

- **Issues:** [GitHub Issues](https://github.com/Xtra01/instagram_downloader/issues)
- **Discussions:** [GitHub Discussions](https://github.com/Xtra01/instagram_downloader/discussions)

---

## 🌟 Teşekkürler / Acknowledgments

- [Instaloader](https://github.com/instaloader/instaloader) - Instagram scraping library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Tailwind CSS](https://tailwindcss.com/) - UI styling

---

**⭐ Projeyi beğendiyseniz yıldız vermeyi unutmayın! / Star the project if you like it!**

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
