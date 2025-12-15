#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Kullanım Örnekleri
Real-world examples for common scenarios
"""

import logging
import sys
from pathlib import Path

# Parent directory'yi path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

from main import (
    InstagramProfileDownloader,
    SessionManager,
    InstagramDownloaderConfig
)
from advanced import InstagramAPIWrapper

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def example_1_basic_download():
    """Örnek 1: Basit profil indirme (oturum olmadan)."""
    logger.info("=" * 60)
    logger.info("Örnek 1: Basit Profil İndirme")
    logger.info("=" * 60)
    
    # Konfigürasyonu yükle
    config = InstagramDownloaderConfig()
    
    # Session Manager'ı başlat
    session_mgr = SessionManager()
    loader = session_mgr.load_or_create()
    
    # Downloader'ı başlat
    downloader = InstagramProfileDownloader(loader, config)
    
    # Profil indir
    try:
        downloader.download_profile(
            username="cristiano",
            max_posts=10,  # İlk 10 post
            download_stories=False
        )
        logger.info("Örnek 1 tamamlandı.")
    except Exception as e:
        logger.error(f"Örnek 1 hata: {e}")


def example_2_authenticated_download():
    """Örnek 2: Oturum açarak indirme (2FA gerekliyse)."""
    logger.info("=" * 60)
    logger.info("Örnek 2: Oturum Açarak İndirme")
    logger.info("=" * 60)
    
    config = InstagramDownloaderConfig()
    session_mgr = SessionManager()
    loader = session_mgr.load_or_create()
    
    # Instagram hesabına giriş yap
    if session_mgr.login("your_instagram_username", "your_password"):
        downloader = InstagramProfileDownloader(loader, config)
        try:
            downloader.download_profile(
                username="target_profile",
                max_posts=50,
                download_stories=True,
                download_highlights=True
            )
            logger.info("Örnek 2 tamamlandı.")
        except Exception as e:
            logger.error(f"Örnek 2 hata: {e}")
    else:
        logger.error("Oturum açılamadı.")


def example_3_advanced_wrapper():
    """Örnek 3: Advanced wrapper ile advanced error handling."""
    logger.info("=" * 60)
    logger.info("Örnek 3: Advanced Wrapper Kullanımı")
    logger.info("=" * 60)
    
    config = InstagramDownloaderConfig()
    session_mgr = SessionManager()
    loader = session_mgr.load_or_create()
    
    # Advanced wrapper oluştur (3 saniye min delay, 5 retry)
    wrapper = InstagramAPIWrapper(
        loader,
        min_delay=3.0,
        max_retries=5
    )
    
    try:
        # Profil al
        profile = wrapper.get_profile("target_profile")
        logger.info(f"Profil Bilgisi: {profile.username} ({profile.followers} takipçi)")
        
        # Posts al (max 30)
        posts = wrapper.get_posts(profile, max_count=30)
        logger.info(f"{len(posts)} post alındı")
        
        # Her post'u indir
        for idx, post in enumerate(posts, 1):
            try:
                wrapper.download_post(post, f"./downloads/target_profile/posts")
                logger.info(f"[{idx}] İndirildi: {post.shortcode}")
            except Exception as e:
                logger.warning(f"[{idx}] Başarısız: {e}")
        
        logger.info("Örnek 3 tamamlandı.")
    
    except Exception as e:
        logger.error(f"Örnek 3 hata: {e}")


def example_4_batch_download():
    """Örnek 4: Toplu indirme (birden fazla profil)."""
    logger.info("=" * 60)
    logger.info("Örnek 4: Toplu İndirme")
    logger.info("=" * 60)
    
    # İndirilecek profil listesi
    profiles_to_download = [
        "cristiano",
        "leomessi",
        "instagram"
    ]
    
    config = InstagramDownloaderConfig()
    session_mgr = SessionManager()
    loader = session_mgr.load_or_create()
    downloader = InstagramProfileDownloader(loader, config)
    
    for profile_name in profiles_to_download:
        try:
            logger.info(f"İndiriliyor: {profile_name}")
            downloader.download_profile(
                username=profile_name,
                max_posts=20,
                download_stories=True
            )
            logger.info(f"Başarı: {profile_name}")
        except Exception as e:
            logger.error(f"Hata {profile_name}: {e}")
    
    logger.info("Örnek 4 tamamlandı.")


def example_5_session_reuse():
    """Örnek 5: Mevcut session'ı yeniden kullan."""
    logger.info("=" * 60)
    logger.info("Örnek 5: Session Yeniden Kullanımı")
    logger.info("=" * 60)
    
    # Eğer daha önce session.pickle oluşturulduysa, otomatik yüklenir
    session_mgr = SessionManager("session.pickle")
    loader = session_mgr.load_or_create()
    
    # Session dosyası varsa, login gerekmez
    config = InstagramDownloaderConfig()
    downloader = InstagramProfileDownloader(loader, config)
    
    try:
        downloader.download_profile(
            username="any_public_profile",
            max_posts=5
        )
        logger.info("Örnek 5 tamamlandı.")
    except Exception as e:
        logger.error(f"Örnek 5 hata: {e}")


def example_6_error_handling():
    """Örnek 6: Hata yönetimi ve exception handling."""
    logger.info("=" * 60)
    logger.info("Örnek 6: Hata Yönetimi")
    logger.info("=" * 60)
    
    from instaloader.exceptions import (
        ProfileNotExistsException,
        PrivateProfileNotFollowedException
    )
    
    config = InstagramDownloaderConfig()
    session_mgr = SessionManager()
    loader = session_mgr.load_or_create()
    downloader = InstagramProfileDownloader(loader, config)
    
    test_profiles = [
        "nonexistent_profile_xyz_123",  # Var olmayan profil
        "private_account_example",       # Özel hesap (variabilir)
        "cristiano"                      # Valid profil
    ]
    
    for profile in test_profiles:
        try:
            logger.info(f"Test: {profile}")
            downloader.download_profile(profile, max_posts=1)
        
        except ProfileNotExistsException:
            logger.warning(f"Profil bulunamadı: {profile}")
        except PrivateProfileNotFollowedException:
            logger.warning(f"Profil özel: {profile}")
        except Exception as e:
            logger.error(f"Beklenmeyen hata {profile}: {type(e).__name__}: {e}")
    
    logger.info("Örnek 6 tamamlandı.")


if __name__ == "__main__":
    """
    Aşağıdaki örneklerden istediğinizi çalıştırın:
    
    Örnek 1: example_1_basic_download()
    Örnek 2: example_2_authenticated_download()
    Örnek 3: example_3_advanced_wrapper()
    Örnek 4: example_4_batch_download()
    Örnek 5: example_5_session_reuse()
    Örnek 6: example_6_error_handling()
    """
    
    # UTF-8 encoding için
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("\n" + "=" * 60)
    print("Instagram Downloader - Kullanım Örnekleri")
    print("=" * 60 + "\n")
    
    print("Mevcut Örnekler:")
    print("1. Basit Profil İndirme")
    print("2. Oturum Açarak İndirme")
    print("3. Advanced Wrapper Kullanımı")
    print("4. Toplu İndirme (Batch)")
    print("5. Session Yeniden Kullanımı")
    print("6. Hata Yönetimi ve Exception Handling")
    print("\n" + "=" * 60 + "\n")
    
    # Çalıştırmak istediğiniz örneği seçin:
    # Uncomment aşağıdaki satırlardan birini:
    
    # example_1_basic_download()
    # example_2_authenticated_download()
    # example_3_advanced_wrapper()
    # example_4_batch_download()
    # example_5_session_reuse()
    # example_6_error_handling()
    
    print("Örnek çalıştırmak için, yukarıdaki satırlardan birinin")
    print("başındaki '#' işaretini kaldırın ve dosyayı çalıştırın.\n")
    
    # Varsayılan olarak Örnek 1'i çalıştır
    logger.info("Varsayılan örnek çalıştırılıyor: Örnek 1 (Basit İndirme)\n")
    example_1_basic_download()
