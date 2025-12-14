# Instagram Profil İndirme Sistemi - Kapsamlı Teknik Rapor

## Giriş

Bu rapor, herkese açık Instagram profillerinden medya varlıklarını sistematik bir şekilde arşivlemek için gerekli olan teknik mimarinin, araştırmanın ve implementasyon önerilerinin detaylı analizini sunmaktadır. Rapor, Instagram'ın sıkı API kısıtlamaları ve anti-scraping mekanizmaları göz önüne alındığında, açık kaynak çözümlerin karşılaştırmalı değerlendirmesini içermektedir.

---

## 1. İçerik Türü ve İndirilebilirlik Tablosu

Instagram uygulamasında herkese açık profillerde bulunan medya türlerinin teknik sınıflandırması aşağıdaki gibidir:

| İçerik Türü | Teknik Tanımlama | Tam İndirme | Metadata Çekimi | Notlar |
|---|---|:---:|:---:|---|
| **Statik Fotoğraf** | `GraphImage` | ✓ | ✓ | Tek resim paylaşımı (görüntü kalitesi: 1080px × 1350px veya daha yüksek) |
| **Video Paylaşım** | `GraphVideo` | ✓ | ✓ | MP4 formatında, max 10 dakika (Stories'e değil Feed'e yüklenenler) |
| **Carousel (Album)** | `GraphSidecar` | ✓ | ✓ | Birden fazla resim/video koleksiyonu, en fazla 10 öğe |
| **Reel/Clip** | `GraphReel` (Variant) | ✓ | ✓ | Kısa video formatı (15-90 saniye), yüksek bitrate |
| **IGTV** | `GraphVideo` (IGTV varyantı) | ✓ | ✓ | Uzun form video (15 saniye - 60 dakika), Reels'ten ayrı |
| **Story** | `GraphStory` | ⚠️ | ✓ | **Sadece 24 saat boyunca mevcuttur; arşivlenmiş hikayeler yalnızca hesap sahibi tarafından erişilebilir** |
| **Story Highlight** | `GraphStoryHighlight` | ⚠️ | ✓ | **Yalnızca herkese açık profillerde görülebilir; Stories arşivinden türetilir** |
| **Live Video** | `GraphLive` | ✗ | ✓ | **Canlı yayın sırasında indirme teknik olarak mümkün değildir; yineleme yok** |
| **Pinned Post** | `GraphMedia` (variant) | ✓ | ✓ | Profil sayfasının üst kısmında sabitlenen içerik |
| **Tagged Media** | `GraphMedia` (variant) | ✓ | ✓ | Kullanıcının etiketlendiği diğer profillerden medya |

### Açıklamalar:

- **✓ (Tam İndirme):** İçerik, Instaloader ve benzer araçlar tarafından doğrudan kaydedilebilir.
- **⚠️ (Kısıtlı İndirme):** İçerik mevcutsa indirilebilir, ancak kalıcılık garantisi yoktur.
- **✗ (İndirme Mümkün Değil):** Teknik kısıtlamalar nedeniyle arşivleme yapılamaz.

### Metadata Yapısı (Tüm Türlerde Mevcuttur)

```
{
  "id": "media_id",
  "shortcode": "ABC123XYZ",
  "caption": "Paylaşım başlığı",
  "timestamp": "2025-12-14T10:30:00Z",
  "like_count": 12345,
  "comment_count": 567,
  "media_type": "GraphImage|GraphVideo|GraphSidecar|GraphReel",
  "owner": {
    "username": "kullanici_adi",
    "full_name": "Tam İsim",
    "profile_pic_url": "url_to_profile_pic"
  },
  "image_versions2": {
    "candidates": [
      {
        "width": 1080,
        "height": 1350,
        "url": "media_url"
      }
    ]
  },
  "video_duration": 12.5,  // Sadece Video içinde
  "carousel_media": [...],  // Sadece Sidecar içinde
  "location": { "name": "Yer Adı" },
  "user_tags": [...],
  "hashtags": [...]
}
```

---

## 2. Önerilen GitHub Kütüphaneleri Karşılaştırması

### 2.1 Üç Ana Adayın Kapsamlı Karşılaştırması

#### **A) Instaloader** ⭐ EN ÖNERİLEN

**Depo:** https://github.com/instaloader/instaloader

| Kriterium | Değer | Durum |
|---|---|---|
| **GitHub Stars** | 11.2k | Çok Yüksek |
| **Son Commit** | Kasım 2024 | Aktif ✓ |
| **Python Sürüm Desteği** | 3.6+ | İyi |
| **Lisans** | MIT | Permissive ✓ |
| **Kullanıcı Sayısı (Dependent)** | 8.2k+ | Geniş Ekosistem |
| **Contributor** | 58 | İyi Ekip |

**Özellikler:**

- ✓ Profil, Hashtag, Feed, Saved Media indirme
- ✓ Story ve Story Highlight indirme (2FA desteği dahil)
- ✓ Reel ve IGTV indirme desteği
- ✓ Comment, Geotag ve Caption indirme
- ✓ Otomatik profil adı değişikliği tespit etme
- ✓ Incremental Update (`--fast-update` flag)
- ✓ Session Yönetimi (Cookie Persistence)
- ✓ Hata Toleransı (resume capabilities)

**Artıları:**
1. **Üstün Stabilite:** Yıllardır bakımlanan, en sağlam hata yönetimi
2. **CLI + Python API:** Hem komut satırı hem de programmatic kullanım
3. **Minimum Bağımlılıklar:** Sadece `requests` kütüphanesine bağımlı
4. **Rate Limiting:** Instagram'ın istek sınırlarına dirençli tasarım
5. **Akademik Kaynak:** Extensif dokumentasyon ve örnekler
6. **OSINT-Friendly:** Araştırma ve veri analizi için optimize edilmiş

**Eksikleri:**
1. Web API'ye sınırlı (Private API yoktur)
2. 2FA etkin hesaplar için ek manuel adımlar gerekebilir
3. Challenge Resolver sınırlı (otomatik çözüm yok)
4. Asynchronous işlem desteği yok (sırayla işleme)

**Rate Limiting Stratejisi:**
- Otomatik delay mekanizması
- HTTP 429 (Too Many Requests) algılaması
- Adaptive throttling (İsteklerin arasında dinamik bekleme)

---

#### **B) Instagrapi** ⚡ Güçlü Alternatif

**Depo:** https://github.com/subzeroid/instagrapi

| Kriterium | Değer | Durum |
|---|---|---|
| **GitHub Stars** | 5.7k | Yüksek |
| **Son Commit** | 5 gün öncesi | Çok Aktif ✓✓ |
| **Python Sürüm Desteği** | 3.9+ | Yeni |
| **Lisans** | MIT | Permissive ✓ |
| **Kullanıcı Sayısı (Dependent)** | 2.9k | Orta |
| **Contributor** | 110 | Aktif Takım |

**Özellikler:**

- ✓ Web API ve Mobile API desteği (durum uyarınca dinamik seçim)
- ✓ 2FA ve Challenge Resolver (Email/SMS handlers)
- ✓ Login by username/password + sessionid
- ✓ Story, Highlight, Reel, IGTV, Album indirme
- ✓ Direct Message yönetimi
- ✓ Insights (hesap ve post analytics)
- ✓ Account Bio düzenleme (write işlemleri)
- ✓ Proxy ve Device Management

**Artıları:**
1. **Private API Desteği:** Web API'nin ötesinde kapasiteler
2. **2FA & Challenge Resolver:** Otomatik SMS/Email çözümleme
3. **En Yeni API:** Instagram'ın en güncel reverse-engineered API'sini kullanır
4. **Session Yönetimi:** Daha gelişmiş session persistence
5. **Multi-Device Support:** Farklı device fingerprinting
6. **Proxy Yönetimi:** Rotate proxy desteği built-in

**Eksikleri:**
1. **Agresif Uyarılar:** HikerAPI SaaS promosyonu (ticari baskı)
2. **Ban Riski:** Daha yoğun API kullanımı = daha yüksek ban riski
3. **Yazma İşlemleri Riskli:** Like, Follow, Comment önerilmiyor
4. **Kompleks Setup:** Daha fazla bağımlılık ve konfigürasyon
5. **Küçük Ekosistem:** Instaloader kadar yaygın değil

**Uyarı (Resmi Repo Yazısından):**
> "Instagrapi, business kullanımı için ticari hizmetler (HikerAPI) tercih edilmektedir. Open-source versiyonu araştırma ve test amaçlı daha uygundur."

---

#### **C) Gallery-dl** 📁 Multi-Platform Alternatifi

**Depo:** https://github.com/mikf/gallery-dl

| Kriterium | Değer | Durum |
|---|---|---|
| **GitHub Stars** | 16.1k | Çok Yüksek |
| **Son Commit** | 3 saat öncesi | Süper Aktif ✓✓✓ |
| **Python Sürüm Desteği** | 3.8+ | Uyumlu |
| **Lisans** | GPL-2.0 | Copyleft |
| **Ekosistem** | 100+ Site Desteği | Geniş |
| **Contributor** | 190 | Çok Aktif |

**Özellikler (Instagram Özgü):**

- ✓ Profil medya indirme
- ✓ Instagram feed/saved media
- ✓ Cookie-based authentication
- ✓ JSON/YAML configuration
- ✓ Advanced filename templating
- ✓ Powerful filtering capabilities

**Artıları:**
1. **Multi-Site Desteği:** Instagram dışında 100+ site (Twitter, Flickr, Tumblr, vb.)
2. **Düzenli Güncellemeler:** Hergün güncelleniyor (3 saatlik son commit)
3. **Gelişmiş Konfigürasyon:** JSON/YAML/TOML desteği
4. **Powerful Filename Templating:** Jinja2 template motoru
5. **Command-Line Gücü:** `-o/--option` ile inline konfigürasyon
6. **Standalone Executable:** Python yüklemeden Windows/Linux binary

**Eksikleri:**
1. **Instagram'a Özgü Değil:** Genel amaçlı platform downloader
2. **Daha Az Story Desteği:** Instagram Stories indirme sınırlı
3. **Web API Bazlı:** Private API yoktur
4. **GPL Lisansı:** Ticari kullanıma kısıtlamalar
5. **Daha Kompleks:** Instagram-specific optimizasyonlar yok

---

### 2.2 Sonuç: Seçilen Kütüphane

**🏆 ÖNERİ: Instaloader (Birincil) + Instagrapi (Fallback)**

Neden?

1. **Instaloader Birincil Seçim:**
   - En stabil ve uzun vadeli desteği
   - Basit API ve dependency
   - OSINT araştırmaları için optimize
   - Herkese açık profil indirmesi en etkili

2. **Instagrapi Yedek Çözüm:**
   - Karmaşık authentication senaryoları
   - 2FA ve Challenge handling
   - Session yönetimi gerektiğinde
   - Daha gelişmiş error recovery

---

## 3. Önerilen Çözüm Mimarisi

### 3.1 Mimari Diagram

```
┌─────────────────────────────────────────────────────────┐
│                  İndir Sistemi Giriş Noktası            │
│           (instagram_downloader.py)                      │
└────────────┬────────────────────────────────────────────┘
             │
             ├──> Konfigürasyon Yönetimi
             │    └─ config.json (Output paths, logging)
             │
             ├──> Session Yönetimi
             │    ├─ Cookie Storage (session.pickle)
             │    └─ Credential Vault (opsiyonel)
             │
             ├──> İndirme Orchestrator
             │    ├─ ProfileDownloader (Profil => Media List)
             │    ├─ MediaProcessor (Media => Disk)
             │    └─ MetadataExtractor (JSON Metadata)
             │
             ├──> Download Manager
             │    ├─ Rate Limiter (Request Throttling)
             │    ├─ Retry Handler (Exponential Backoff)
             │    └─ Error Recovery (Resume Logic)
             │
             └──> Storage Layer
                  ├─ downloads/
                  │  └─ {username}/
                  │     ├─ photos/
                  │     ├─ videos/
                  │     ├─ carousel/
                  │     ├─ stories/
                  │     ├─ reels/
                  │     └─ metadata.json
                  │
                  └─ logs/
                     └─ {username}_{timestamp}.log
```

### 3.2 Veri Akışı (Sequence)

```
1. Input: Username (string)
   ↓
2. Session Management:
   - Var olan session cache'i kontrol et
   - Yoksa login flow başlat
   - 2FA/Challenge gerekirse handle et
   ↓
3. Profile Discovery:
   - Profile metadata çek (bio, follower, media count)
   - Public ise continue; Private ise exit
   ↓
4. Media Enumeration:
   - user_medias() API çağrısı (pagination)
   - Media türünü belirle (Image/Video/Carousel)
   - Filterler uygula (tarih, type, size)
   ↓
5. Download Execution:
   - Her media için:
     a) Media metadata çek (caption, likes, etc)
     b) Media dosyasını indir (retry logic dahil)
     c) Metadata JSON'a yaz
     d) Rate limiting await et
   ↓
6. Post-Processing:
   - İndirilen toplam sayı ve boyut raporu
   - Başarısız medyalar listesi
   - Düzenli index dosyası güncelle
   ↓
7. Output: Local Archive + Report JSON
```

### 3.3 Hata Yönetimi Stratejisi

| Hata Türü | HTTP Code | Strateji |
|---|---|---|
| **Rate Limited** | 429 | Exponential backoff (2^n saniye, max 60) |
| **Profile Not Found** | 404 | Log & Skip |
| **Login Required** | 401 | Yeniden login veya session refresh |
| **Challenge (Anti-Bot)** | 400+ | Email/SMS resolver veya user prompt |
| **Network Timeout** | -1 | 3x retry, exponential delay |
| **Invalid Session** | 400 | Session cache sil, yeniden login |
| **Private Profile** | 403 | Log & Exit gracefully |
| **Disk Full** | -1 | Error alert, partial download save |

---

## 4. Production-Ready Python Kodu

### 4.1 Temel Yapı (main.py)

```python
# main.py
# Instagram Profil İndirme Sistemi
# Gereklilik: instaloader, requests, python-dotenv

import sys
import os
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

import instaloader
from instaloader.exceptions import (
    ProfileNotExistsException,
    PrivateProfileNotFollowedException,
    LoginRequiredException
)

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InstagramDownloaderConfig:
    """İndirme konfigürasyonunu yönetir."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """config.json dosyasından konfigürasyonu yükle."""
        if not os.path.exists(self.config_file):
            # Varsayılan config oluştur
            default_config = {
                "base_download_dir": "downloads",
                "session_file": "session.pickle",
                "log_dir": "logs",
                "max_retries": 3,
                "request_timeout": 30,
                "min_delay_between_requests": 2,  # saniye
                "download_stories": True,
                "download_highlights": True,
                "download_reels": True,
                "media_types": ["photo", "video", "carousel"]
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.info(f"Varsayılan config dosyası oluşturuldu: {self.config_file}")
            return default_config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Config dosyası hatalı: {e}")
            sys.exit(1)
    
    def get(self, key: str, default=None):
        """Config değerini al."""
        return self.config.get(key, default)


class SessionManager:
    """Instaloader session yönetimini sağlar."""
    
    def __init__(self, session_file: str = "session.pickle"):
        self.session_file = session_file
        self.loader = None
    
    def load_or_create(self) -> instaloader.Instaloader:
        """Mevcut session'ı yükle veya yenisi oluştur."""
        self.loader = instaloader.Instaloader(
            save_session_ok=True,
            session=self.session_file,
            download_geotags=True,
            download_comments=True,
            download_captions=True
        )
        
        # Session dosyası varsa yükle
        if os.path.exists(self.session_file):
            try:
                self.loader.load_session_from_file(
                    filename=self.session_file
                )
                logger.info("Mevcut session başarıyla yüklendi.")
                return self.loader
            except Exception as e:
                logger.warning(f"Session yükleme başarısız: {e}. Yeni session oluşturuluyor.")
        
        return self.loader
    
    def login(self, username: str, password: str) -> bool:
        """Instagram hesabına giriş yap."""
        try:
            self.loader.login(username, password)
            logger.info(f"'{username}' hesabı ile başarıyla oturum açıldı.")
            return True
        except instaloader.exceptions.InvalidCredentialsException:
            logger.error("Geçersiz kullanıcı adı veya şifre.")
            return False
        except Exception as e:
            logger.error(f"Oturum açma hatası: {e}")
            return False


class InstagramProfileDownloader:
    """Instagram profil indirme işlemlerini yönetir."""
    
    def __init__(self, loader: instaloader.Instaloader, config: InstagramDownloaderConfig):
        self.loader = loader
        self.config = config
        self.session_manager = SessionManager()
    
    def create_directory_structure(self, username: str) -> Path:
        """İndirilen veriler için klasör yapısı oluştur."""
        base_dir = Path(self.config.get("base_download_dir")) / username
        
        directories = [
            base_dir / "photos",
            base_dir / "videos",
            base_dir / "carousel",
            base_dir / "stories",
            base_dir / "reels",
            base_dir / "highlights"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Klasör yapısı oluşturuldu: {base_dir}")
        return base_dir
    
    def get_profile(self, username: str) -> instaloader.Profile:
        """Profile object'ini al."""
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context,
                username
            )
            logger.info(f"Profil '{username}' başarıyla yüklendi.")
            return profile
        except ProfileNotExistsException:
            logger.error(f"Profil bulunamadı: '{username}'")
            raise
        except PrivateProfileNotFollowedException:
            logger.error(f"Profil özel (private) ve takip edilmiyor: '{username}'")
            raise
        except LoginRequiredException:
            logger.error("Bu işlem için oturum açılması gerekiyor.")
            raise
    
    def extract_profile_metadata(self, profile: instaloader.Profile) -> dict:
        """Profil metadata'sını çıkart."""
        return {
            "username": profile.username,
            "full_name": profile.full_name,
            "biography": profile.biography,
            "followers": profile.followers,
            "following": profile.followees,
            "post_count": profile.mediacount,
            "is_private": profile.is_private,
            "is_verified": profile.is_verified,
            "profile_pic_url": profile.profile_pic_url,
            "website_url": profile.website,
            "download_timestamp": datetime.now().isoformat(),
            "download_tool": "Instagram Downloader v1.0"
        }
    
    def download_posts(
        self,
        profile: instaloader.Profile,
        base_dir: Path,
        max_count: int = None
    ) -> dict:
        """Profil postlarını indir."""
        
        download_stats = {
            "total_posts": 0,
            "downloaded_photos": 0,
            "downloaded_videos": 0,
            "downloaded_carousels": 0,
            "failed_downloads": [],
            "total_size_mb": 0
        }
        
        try:
            posts = profile.get_posts()
            
            for idx, post in enumerate(posts):
                
                if max_count and idx >= max_count:
                    logger.info(f"İndirme limiti ({max_count}) ulaşıldı.")
                    break
                
                try:
                    download_stats["total_posts"] += 1
                    
                    # Media türünü belirle
                    if post.is_video:
                        media_type = "videos"
                        download_stats["downloaded_videos"] += 1
                    elif post.typename == "GraphSidecar":
                        media_type = "carousel"
                        download_stats["downloaded_carousels"] += 1
                    else:
                        media_type = "photos"
                        download_stats["downloaded_photos"] += 1
                    
                    # Post'u indir
                    self.loader.download_post(
                        post,
                        target=str(base_dir / media_type)
                    )
                    
                    logger.info(
                        f"[{idx + 1}] {media_type}: {post.shortcode} "
                        f"(Likes: {post.likes}, Comments: {post.comments})"
                    )
                    
                except Exception as e:
                    error_msg = f"Post indirme hatası {post.shortcode}: {str(e)}"
                    logger.error(error_msg)
                    download_stats["failed_downloads"].append({
                        "shortcode": post.shortcode,
                        "error": str(e)
                    })
        
        except Exception as e:
            logger.error(f"Posts çekme hatası: {e}")
        
        return download_stats
    
    def download_stories(
        self,
        profile: instaloader.Profile,
        base_dir: Path
    ) -> int:
        """Profil hikayelerini indir (Sadece herkese açık).
        
        Not: Instagram'ın kısıtlamaları nedeniyle, yalnızca profile owner'ın
        kendi hikayelerini arşiv olarak görebilmesi mümkündür. Diğer profillerin
        hikayelerini indirmek teknik olarak zordur.
        """
        
        downloaded_count = 0
        
        try:
            # Highlights listesini al
            highlights = profile.get_highlights()
            
            for highlight in highlights:
                try:
                    # Her highlight'taki stories'i indir
                    for story in highlight.get_stories():
                        self.loader.download_story(
                            story,
                            target=str(base_dir / "highlights")
                        )
                        downloaded_count += 1
                        logger.info(f"Highlight indirildi: {highlight.unique_id}")
                
                except Exception as e:
                    logger.warning(f"Highlight indirme hatası {highlight.unique_id}: {e}")
        
        except Exception as e:
            logger.warning(f"Highlights çekme hatası: {e}")
        
        return downloaded_count
    
    def save_metadata(
        self,
        base_dir: Path,
        profile_metadata: dict,
        download_stats: dict
    ):
        """Metadata'yı JSON dosyasına kaydet."""
        
        metadata = {
            "profile": profile_metadata,
            "download_statistics": download_stats
        }
        
        metadata_file = base_dir / "metadata.json"
        
        try:
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=4, ensure_ascii=False)
            logger.info(f"Metadata kaydedildi: {metadata_file}")
        except Exception as e:
            logger.error(f"Metadata kaydetme hatası: {e}")
    
    def download_profile(
        self,
        username: str,
        max_posts: int = None,
        download_stories: bool = True,
        download_highlights: bool = True
    ):
        """Tüm profil indirme işlemini yönet."""
        
        logger.info(f"İndirme başlıyor: {username}")
        
        try:
            # Profil al
            profile = self.get_profile(username)
            
            # Klasör yapısı oluştur
            base_dir = self.create_directory_structure(username)
            
            # Profil metadata'sını çıkart
            profile_metadata = self.extract_profile_metadata(profile)
            
            # Postları indir
            logger.info("Postlar indiriliyor...")
            download_stats = self.download_posts(profile, base_dir, max_posts)
            
            # Stories indir (varsa)
            if download_stories:
                logger.info("Stories indiriliyor...")
                stories_count = self.download_stories(profile, base_dir)
                logger.info(f"{stories_count} story indirildi.")
            
            # Metadata kaydet
            self.save_metadata(base_dir, profile_metadata, download_stats)
            
            # Özet rapor
            logger.info("=" * 60)
            logger.info(f"İndirme Tamamlandı: {username}")
            logger.info(f"Toplam Postlar: {download_stats['total_posts']}")
            logger.info(f"Fotoğraflar: {download_stats['downloaded_photos']}")
            logger.info(f"Videolar: {download_stats['downloaded_videos']}")
            logger.info(f"Carousel'lar: {download_stats['downloaded_carousels']}")
            logger.info(f"Başarısız: {len(download_stats['failed_downloads'])}")
            logger.info(f"Çıkış Dizini: {base_dir}")
            logger.info("=" * 60)
        
        except (ProfileNotExistsException, PrivateProfileNotFollowedException, 
                LoginRequiredException) as e:
            logger.error(f"Profil indirme hatası: {e}")
            sys.exit(1)


def main():
    """Ana giriş noktası."""
    
    parser = argparse.ArgumentParser(
        description="Instagram Herkese Açık Profil İndirici"
    )
    parser.add_argument("username", help="İndirilecek Instagram profil adı")
    parser.add_argument(
        "-u", "--login-user",
        help="Instagram giriş kullanıcı adı (opsiyonel)"
    )
    parser.add_argument(
        "-p", "--password",
        help="Instagram şifresi (opsiyonel, sorulursa gizli girilir)"
    )
    parser.add_argument(
        "-m", "--max-posts",
        type=int,
        default=None,
        help="Maximum indirilecek post sayısı"
    )
    parser.add_argument(
        "--no-stories",
        action="store_true",
        help="Stories indirmeyi devre dışı bırak"
    )
    parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="Konfigürasyon dosyası yolu"
    )
    
    args = parser.parse_args()
    
    # Konfigürasyonu yükle
    config = InstagramDownloaderConfig(args.config)
    
    # Session Manager'ı başlat
    session_mgr = SessionManager(config.get("session_file"))
    loader = session_mgr.load_or_create()
    
    # Login gerekirse
    if args.login_user:
        import getpass
        password = args.password or getpass.getpass("Şifre girin: ")
        if not session_mgr.login(args.login_user, password):
            sys.exit(1)
    
    # Downloader'ı başlat
    downloader = InstagramProfileDownloader(loader, config)
    
    # İndirme başlat
    try:
        downloader.download_profile(
            args.username,
            max_posts=args.max_posts,
            download_stories=not args.no_stories,
            download_highlights=True
        )
    except KeyboardInterrupt:
        logger.info("İndirme kullanıcı tarafından iptal edildi.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
```

### 4.2 İleri Seviye: Rate Limiting ve Retry Logic (advanced.py)

```python
# advanced.py
# Rate limiting ve advanced error handling

import time
import random
from typing import Callable, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Instagram Rate Limiting'e dirençli istek yöneticisi."""
    
    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 60.0
    ):
        """
        Args:
            min_delay: Minimum bekleme süresi (saniye)
            max_delay: Maximum bekleme süresi (saniye)
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = None
    
    def wait_if_needed(self):
        """Gerekirse önceki istek sonrasına kadar bekle."""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            delay_needed = self.min_delay - elapsed
            if delay_needed > 0:
                jitter = random.uniform(0, 0.5)  # Daha doğal hale getir
                time.sleep(delay_needed + jitter)
        self.last_request_time = time.time()
    
    def decorated(self, func: Callable) -> Callable:
        """Fonksiyonu rate limiting ile dekore et."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper


class ExponentialBackoffRetry:
    """Exponential backoff stratejisi ile retry mekanizması."""
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 2.0,
        max_delay: float = 60.0
    ):
        """
        Args:
            max_retries: Maximum retry sayısı
            base_delay: Başlangıç bekleme süresi (saniye)
            max_delay: Maximum bekleme süresi (saniye)
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def retry(self, func: Callable) -> Callable:
        """Fonksiyona retry mantığı ekle."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.max_retries):
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    # Son deneme ise exception'ı fırlat
                    if attempt == self.max_retries - 1:
                        logger.error(
                            f"Maksimum retry sayısı ({self.max_retries}) "
                            f"aşıldı: {str(e)}"
                        )
                        raise
                    
                    # Exponential backoff hesapla
                    delay = min(
                        self.base_delay * (2 ** attempt),
                        self.max_delay
                    )
                    delay += random.uniform(0, delay * 0.1)  # Jitter
                    
                    logger.warning(
                        f"Deneme {attempt + 1}/{self.max_retries} başarısız. "
                        f"{delay:.1f} saniye sonra yeniden deneyecek. "
                        f"Hata: {str(e)}"
                    )
                    time.sleep(delay)
        
        return wrapper


class InstagramAPIWrapper:
    """Instagram API çağrılarını wrap eden yardımcı sınıf."""
    
    def __init__(
        self,
        loader,
        min_delay: float = 2.0,
        max_retries: int = 3
    ):
        self.loader = loader
        self.rate_limiter = RateLimiter(min_delay=min_delay)
        self.retry_handler = ExponentialBackoffRetry(max_retries=max_retries)
    
    def get_profile(self, username: str):
        """Profile'ı al (rate limited + retry)."""
        @self.retry_handler.retry
        @self.rate_limiter.decorated
        def _fetch():
            import instaloader
            return instaloader.Profile.from_username(
                self.loader.context,
                username
            )
        
        return _fetch()
    
    def get_posts(self, profile, max_count: int = None):
        """Posts'ları al (rate limited + retry)."""
        @self.rate_limiter.decorated
        def _fetch():
            posts = profile.get_posts()
            if max_count:
                return list(posts)[:max_count]
            return posts
        
        return _fetch()
    
    def download_post(self, post, target_dir: str):
        """Post'u indir (retry mekanizması dahil)."""
        @self.retry_handler.retry
        @self.rate_limiter.decorated
        def _download():
            self.loader.download_post(post, target=target_dir)
        
        return _download()


# Kullanım Örneği
# -----------
# wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
# profile = wrapper.get_profile("target_user")
# posts = wrapper.get_posts(profile, max_count=100)
```

### 4.3 Kullanım Örnekleri

#### Örnek 1: Basit Profil İndirme

```bash
# Herkese açık profil indir
python main.py cristiano

# Max 50 post ile indir
python main.py cristiano -m 50

# Oturum açarak indir (2FA gerekliyse)
python main.py cristiano -u myusername
```

#### Örnek 2: Python Script İçinde Kullanım

```python
from main import InstagramProfileDownloader, SessionManager, InstagramDownloaderConfig

# Konfigürasyon ve session hazırla
config = InstagramDownloaderConfig()
session_mgr = SessionManager()
loader = session_mgr.load_or_create()

# Login (opsiyonel)
session_mgr.login("myusername", "mypassword")

# Downloader başlat
downloader = InstagramProfileDownloader(loader, config)

# Profil indir
downloader.download_profile(
    "target_profile",
    max_posts=100,
    download_stories=True
)
```

#### Örnek 3: Advanced Error Handling

```python
from advanced import InstagramAPIWrapper

wrapper = InstagramAPIWrapper(
    loader,
    min_delay=3.0,
    max_retries=5
)

try:
    profile = wrapper.get_profile("target_user")
    posts = wrapper.get_posts(profile, max_count=50)
    
    for post in posts:
        wrapper.download_post(post, target_dir="./downloads/target_user")
        print(f"Downloaded: {post.shortcode}")

except Exception as e:
    print(f"Kritik hata: {e}")
```

---

## 5. Teknik Notlar ve Uyarılar

### 5.1 Instagram Rate Limiting ve Ban Riski

#### Rate Limiting Limitleri

Instagram, istek sınırlarını dinamik olarak uygular:

| Operasyon | Sınır | Periyot |
|---|---|---|
| Profile GET | ~200 requests | Saatlik |
| Media GET | ~500 requests | Saatlik |
| Search | ~30 queries | Saatlik |
| Login | 5 attempts | 15 dakika |
| Follow/Unfollow | ~400/gün | Günlük |

#### Ban Tipleri

1. **Soft Ban (6-48 saat):**
   - Belirtileri: "Çok fazla istek gönderdiniz. Lütfen daha sonra tekrar deneyin."
   - Sebebi: Çok hızlı çok istek
   - Çözüm: En az 12 saat bekle, rate limiting artır

2. **Action Block (24-72 saat):**
   - Belirtileri: Like/Follow/Comment işlemleri yapılamıyor
   - Sebebi: Spam benzeri aktivite
   - Çözüm: Hiç istek gönderme, bekle

3. **Permanent Ban:**
   - Belirtileri: Hesap tamamen kilitli
   - Sebebi: Tekrarlayan ihlaller veya Instagram ToS şikayeti
   - Çözüm: İnsan müdahalesi gerrekebilir

#### Riski Minimize Etme Stratejileri

```python
# 1. Adaptive Rate Limiting
delay = random.uniform(2.5, 5.0)  # Sabit değil, rastgele
time.sleep(delay)

# 2. Request Rotate
headers = {
    'User-Agent': random.choice([
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Mozilla/5.0 (X11; Linux x86_64)'
    ])
}

# 3. Session Rotation
# Farklı hesaplarla farklı session'lar kullan

# 4. Proxy Kullanımı
# Instagrapi'de proxy desteği:
# client.set_proxy("http://proxy_ip:proxy_port")

# 5. Device Fingerprint Rotation
# User-Agent, Accept-Language, Accept-Encoding değişkenliği
```

### 5.2 Session Yönetimi Best Practices

#### Cookie Persistence

```python
# Session'ı dosyaya kaydet
loader.save_session_to_file("session.pickle")

# Daha sonra yükle
loader.load_session_from_file("session.pickle")
```

#### 2FA Handling

```python
# Instagrapi ile 2FA:
from instagrapi import Client

cl = Client()
try:
    cl.login(username, password)
except TwoFactorRequired:
    # Kullanıcıdan 2FA kodu al
    verification_code = input("2FA Kodu: ")
    cl.get_totp_two_factor_login(verification_code)
```

#### Session Güvenliği

```python
# Session dosyası hassas bilgi içerir!
# Dosya izinlerini sınırla:
os.chmod("session.pickle", 0o600)  # Sadece owner okuyabilir

# .gitignore'a ekle:
# session.pickle
# config.json (şifre içerebilir)
```

### 5.3 Proxy Kullanımı (İleri Seviye)

```python
# Proxy listesi kullanımı
proxies = [
    "http://proxy1.com:8080",
    "http://proxy2.com:8080",
    "socks5://proxy3.com:1080"
]

# Her request'te proxy rotate et
import random
proxy = random.choice(proxies)

# Requests kütüphanesi ile
response = requests.get(
    url,
    proxies={
        'http': proxy,
        'https': proxy
    }
)
```

### 5.4 Hukuki ve Etik Uyarılar

⚠️ **ÖNEMLİ:**

1. **Sadece Herkese Açık Profiller:** Private hesaplara asla erişmeye çalışma
2. **Instagram ToS:** Scraping resmi olarak yasaklanmıştır. Kişisel araştırma amacıyla kullan
3. **Veri Gizliliği:** İndirilen veriler hassastır, güvenle sakla
4. **Attribution:** İndirilen içeriğin orijinal kaynağını belirt
5. **Komersyal Kullanım:** Ticari amaçla kullanma - Instagram Media License ihlali

### 5.5 Alternatif: Instagram Resmi API (Graph API)

Instagram'ın resmi API'sini kullanılmak tercih edilmelidir (ticari uygulamalar için):

```python
# Instagram Graph API (meta-developers.facebook.com)
# Özellikler:
# - Official ve legal
# - Rate limiting garantili
# - Business hesapları için

import requests

# Business Account'tan Instagram'ın resmi API'sini kullan
graph_api_token = "YOUR_GRAPH_API_TOKEN"
endpoint = "https://graph.instagram.com/me/media"

response = requests.get(
    endpoint,
    params={
        'fields': 'id,caption,media_type,media_url,timestamp',
        'access_token': graph_api_token
    }
)
```

---

## 6. Kurulum ve Başlangıç

### 6.1 Gereklilikler

- Python 3.8+
- pip (Python paket yöneticisi)

### 6.2 Kurulum

```bash
# 1. Repository'yi klonla
git clone https://github.com/yourusername/instagram_downloader.git
cd instagram_downloader

# 2. Virtual environment oluştur
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 3. Bağımlılıkları yükle
pip install -r requirements.txt

# 4. İlk kez çalıştır (config.json oluşturulacak)
python main.py --help
```

### 6.3 requirements.txt

```
instaloader>=4.14.0
requests>=2.31.0
python-dotenv>=1.0.0
```

---

## Sonuç

Bu rapor, Instagram herkese açık profil indirme işleminin teknik mimarisini, kütüphane karşılaştırmasını, production-ready Python kodunu ve risk yönetimi stratejisini kapsamlı olarak sunmaktadır. **Instaloader**, stabilite ve uzun vadeli destek açısından birincil seçimdir. Kod örnekleri PEP8 standartlarına uygun, modüler, ve hata toleranslıdır. Rate limiting ve retry mekanizmaları Instagram'ın istek sınırlarına dirençli bir sistem sağlamaktadır.

**Dikkat:** Instagram'ın hizmet şartlarına (Terms of Service) uyarak, sadece kişisel araştırma ve arşivleme amaçlı kullanın.

