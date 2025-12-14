#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Advanced Rate Limiting ve Error Handling
Instagram İndirme Sistemi için İleri Seviye Özellikler

Kullanım:
    from advanced import InstagramAPIWrapper, RateLimiter, ExponentialBackoffRetry
    
    wrapper = InstagramAPIWrapper(loader, min_delay=3.0, max_retries=5)
    profile = wrapper.get_profile("username")
"""

import time
import random
import logging
from typing import Callable, Any
from functools import wraps

logger = logging.getLogger(__name__)


class RateLimiter:
    """Instagram Rate Limiting'e dirençli istek yöneticisi.
    
    Instagram'ın istek sınırlarını aşmamak için adaptive delay
    mekanizmasını uygulamaktadır.
    """
    
    def __init__(
        self,
        min_delay: float = 2.0,
        max_delay: float = 60.0
    ):
        """
        Args:
            min_delay (float): Minimum bekleme süresi (saniye)
            max_delay (float): Maximum bekleme süresi (saniye)
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = None
    
    def wait_if_needed(self):
        """Gerekirse önceki istek sonrasına kadar bekle.
        
        Instagram'ı sabit pattern'lardan kaçındırır (daha doğal görünür).
        """
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            delay_needed = self.min_delay - elapsed
            if delay_needed > 0:
                # Jitter: Sabit delay yerine rastgele ekle
                jitter = random.uniform(0, 0.5)
                actual_delay = delay_needed + jitter
                logger.debug(f"Rate limiting: {actual_delay:.2f}s bekleniyor.")
                time.sleep(actual_delay)
        self.last_request_time = time.time()
    
    def decorated(self, func: Callable) -> Callable:
        """Fonksiyonu rate limiting ile dekore et.
        
        Args:
            func (Callable): Dekore edilecek fonksiyon
            
        Returns:
            Callable: Rate limited fonksiyon
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.wait_if_needed()
            return func(*args, **kwargs)
        return wrapper


class ExponentialBackoffRetry:
    """Exponential backoff stratejisi ile retry mekanizması.
    
    Hata durumunda, bekleme süresini 2^n algoritması ile artırır.
    """
    
    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 2.0,
        max_delay: float = 60.0
    ):
        """
        Args:
            max_retries (int): Maximum retry sayısı
            base_delay (float): Başlangıç bekleme süresi (saniye)
            max_delay (float): Maximum bekleme süresi (saniye)
            
        Örnek (3 retry, base_delay=2):
            - Attempt 1: 2s bekle (2^0 = 1 * 2)
            - Attempt 2: 4s bekle (2^1 = 2 * 2)
            - Attempt 3: 8s bekle (2^2 = 4 * 2)
            - Max 60s
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
    
    def retry(self, func: Callable) -> Callable:
        """Fonksiyona retry mantığı ekle.
        
        Args:
            func (Callable): Dekore edilecek fonksiyon
            
        Returns:
            Callable: Retry mekanizmasıyla fonksiyon
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(self.max_retries):
                try:
                    logger.debug(f"{func.__name__} çalıştırılıyor (attempt {attempt + 1}/{self.max_retries})")
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    
                    # Son deneme ise exception'ı fırlat
                    if attempt == self.max_retries - 1:
                        logger.error(
                            f"Maksimum retry sayısı ({self.max_retries}) "
                            f"aşıldı: {func.__name__}. Hata: {str(e)}"
                        )
                        raise
                    
                    # Exponential backoff hesapla: base_delay * 2^attempt
                    delay = min(
                        self.base_delay * (2 ** attempt),
                        self.max_delay
                    )
                    # Jitter ekle (%0-10 varyasyon)
                    delay += random.uniform(0, delay * 0.1)
                    
                    logger.warning(
                        f"Deneme {attempt + 1}/{self.max_retries} başarısız. "
                        f"{func.__name__}: {delay:.1f}s sonra yeniden deneyecek. "
                        f"Hata: {type(e).__name__}: {str(e)}"
                    )
                    time.sleep(delay)
        
        return wrapper


class InstagramAPIWrapper:
    """Instagram API çağrılarını wrap eden yardımcı sınıf.
    
    Tüm API çağrılarına rate limiting ve retry mekanizması ekler.
    """
    
    def __init__(
        self,
        loader,
        min_delay: float = 2.0,
        max_retries: int = 3
    ):
        """
        Args:
            loader: Instaloader instance
            min_delay (float): Minimum bekleme süresi (saniye)
            max_retries (int): Maximum retry sayısı
        """
        self.loader = loader
        self.rate_limiter = RateLimiter(min_delay=min_delay)
        self.retry_handler = ExponentialBackoffRetry(max_retries=max_retries)
        
        logger.info(
            f"InstagramAPIWrapper başlatıldı. "
            f"min_delay={min_delay}s, max_retries={max_retries}"
        )
    
    def get_profile(self, username: str):
        """Profile'ı al (rate limited + retry).
        
        Args:
            username (str): Instagram kullanıcı adı
            
        Returns:
            instaloader.Profile: Profile object
            
        Raises:
            Exception: Hata meydana gelirse
        """
        @self.retry_handler.retry
        @self.rate_limiter.decorated
        def _fetch():
            import instaloader
            profile = instaloader.Profile.from_username(
                self.loader.context,
                username
            )
            logger.info(f"Profile yüklendi: {username} ({profile.followers} followers)")
            return profile
        
        return _fetch()
    
    def get_posts(self, profile, max_count: int = None):
        """Posts'ları al (rate limited + retry).
        
        Args:
            profile: instaloader.Profile object
            max_count (int): Maximum post sayısı
            
        Returns:
            list: Posts listesi
        """
        @self.rate_limiter.decorated
        def _fetch():
            posts = profile.get_posts()
            posts_list = list(posts)
            if max_count:
                posts_list = posts_list[:max_count]
            logger.info(f"{len(posts_list)} post alındı")
            return posts_list
        
        return _fetch()
    
    def download_post(self, post, target_dir: str):
        """Post'u indir (retry mekanizması dahil).
        
        Args:
            post: instaloader.Post object
            target_dir (str): İndirme dizini
        """
        @self.retry_handler.retry
        @self.rate_limiter.decorated
        def _download():
            self.loader.download_post(post, target=target_dir)
            logger.info(f"Post indirildi: {post.shortcode}")
        
        return _download()
    
    def download_story(self, story, target_dir: str):
        """Story'i indir (retry mekanizması dahil).
        
        Args:
            story: instaloader.Story object
            target_dir (str): İndirme dizini
        """
        @self.retry_handler.retry
        @self.rate_limiter.decorated
        def _download():
            self.loader.download_story(story, target=target_dir)
            logger.info(f"Story indirildi: {story.owner_username}")
        
        return _download()
    
    def download_profile_posts(
        self,
        username: str,
        target_dir: str,
        max_count: int = None
    ) -> dict:
        """Profil postlarını in indir (üst seviye işlem).
        
        Args:
            username (str): Instagram kullanıcı adı
            target_dir (str): İndirme dizini
            max_count (int): Maximum post sayısı
            
        Returns:
            dict: İndirme istatistikleri
        """
        stats = {
            "total_downloaded": 0,
            "total_failed": 0,
            "failed_posts": []
        }
        
        try:
            profile = self.get_profile(username)
            posts = self.get_posts(profile, max_count)
            
            for idx, post in enumerate(posts, 1):
                try:
                    self.download_post(post, target_dir)
                    stats["total_downloaded"] += 1
                    logger.info(f"[{idx}/{len(posts)}] Başarı")
                except Exception as e:
                    stats["total_failed"] += 1
                    stats["failed_posts"].append({
                        "shortcode": post.shortcode,
                        "error": str(e)
                    })
                    logger.error(f"[{idx}/{len(posts)}] Başarısız: {e}")
        
        except Exception as e:
            logger.error(f"Profil indirme işlemi hatası: {e}")
        
        return stats


# Örnek Kullanım
# ==============
if __name__ == "__main__":
    # Logging konfigürasyonu
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Not: Bu dosyayı doğrudan çalıştırmak için:
    # python advanced.py
    
    # Gerçek kullanım:
    # from main import SessionManager, InstagramDownloaderConfig
    # from advanced import InstagramAPIWrapper
    # 
    # config = InstagramDownloaderConfig()
    # session_mgr = SessionManager()
    # loader = session_mgr.load_or_create()
    # session_mgr.login("username", "password")
    # 
    # wrapper = InstagramAPIWrapper(
    #     loader,
    #     min_delay=3.0,
    #     max_retries=5
    # )
    # 
    # stats = wrapper.download_profile_posts(
    #     "target_username",
    #     "/path/to/download",
    #     max_count=50
    # )
    # 
    # print(f"İndirilen: {stats['total_downloaded']}")
    # print(f"Başarısız: {stats['total_failed']}")
    
    print("Advanced modul. Docs: Dosya başında yorum satırlarına bakın.")
