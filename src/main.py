#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Herkese Açık Profil İndirici
Version: 1.0.0
Python: 3.8+

Gereklilik: instaloader, requests, python-dotenv

Kullanım:
    python main.py <username> [options]

Örnek:
    python main.py cristiano
    python main.py cristiano -m 50 -u myusername
"""

import sys
import os
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

# UTF-8 encoding için (Windows PowerShell)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

try:
    import instaloader
    from instaloader.exceptions import (
        ProfileNotExistsException,
        PrivateProfileNotFollowedException,
        LoginRequiredException
    )
except ImportError:
    print("Hata: instaloader kütüphanesi yüklü değil.")
    print("Kurulum: pip install instaloader")
    sys.exit(1)

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class InstagramDownloaderConfig:
    """İndirme konfigürasyonunu yönetir."""
    
    def __init__(self, config_file: str = "config.json"):
        """
        Args:
            config_file (str): Konfigürasyon dosyası yolu
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """config.json dosyasından konfigürasyonu yükle."""
        # Config dosyası path'ini düzelt (root veya config klasöründe olabilir)
        config_paths = [
            self.config_file,  # Verilen path
            os.path.join(os.path.dirname(__file__), "..", self.config_file),  # Root
            os.path.join(os.path.dirname(__file__), "..", "config", self.config_file.replace("config.json", "config.json.example"))  # config/
        ]
        
        config_file_found = None
        for path in config_paths:
            if os.path.exists(path):
                config_file_found = path
                break
        
        if not config_file_found:
            # Varsayılan config oluştur (root'ta)
            root_config = os.path.join(os.path.dirname(__file__), "..", self.config_file)
            default_config = {
                "base_download_dir": "downloads",
                "session_file": "session.pickle",
                "log_dir": "logs",
                "max_retries": 3,
                "request_timeout": 30,
                "min_delay_between_requests": 2,
                "download_stories": True,
                "download_highlights": True,
                "download_reels": True,
                "media_types": ["photo", "video", "carousel"]
            }
            os.makedirs(os.path.dirname(root_config), exist_ok=True)
            with open(root_config, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4, ensure_ascii=False)
            logger.info(f"Varsayılan config dosyası oluşturuldu: {root_config}")
            self.config_file = root_config
            return default_config
        
        try:
            with open(config_file_found, 'r', encoding='utf-8') as f:
                self.config_file = config_file_found
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
        """
        Args:
            session_file (str): Session dosyası yolu
        """
        self.session_file = session_file
        self.loader = None
    
    def load_or_create(self) -> instaloader.Instaloader:
        """Mevcut session'ı yükle veya yenisi oluştur."""
        self.loader = instaloader.Instaloader(
            download_geotags=True,
            download_comments=True,
            save_metadata=True,
            compress_json=False
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
        """Instagram hesabına giriş yap.
        
        Args:
            username (str): Instagram kullanıcı adı
            password (str): Instagram şifresi
            
        Returns:
            bool: Başarılı ise True
        """
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
        """
        Args:
            loader (instaloader.Instaloader): Instaloader instance
            config (InstagramDownloaderConfig): Konfigürasyon
        """
        self.loader = loader
        self.config = config
    
    def create_directory_structure(self, username: str) -> Path:
        """İndirilen veriler için klasör yapısı oluştur.
        
        Args:
            username (str): Instagram kullanıcı adı
            
        Returns:
            Path: Ana klasör yolu
        """
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
        """Profile object'ini al.
        
        Args:
            username (str): Instagram profil adı
            
        Returns:
            instaloader.Profile: Profile object
            
        Raises:
            ProfileNotExistsException: Profil bulunamadı
            PrivateProfileNotFollowedException: Özel profil
            LoginRequiredException: Oturum açılması gerekiyor
        """
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
        """Profil metadata'sını çıkart.
        
        Args:
            profile (instaloader.Profile): Profile object
            
        Returns:
            dict: Profil metadata'sı
        """
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
            "external_url": getattr(profile, 'external_url', None),  # API değişikliği
            "download_timestamp": datetime.now().isoformat(),
            "download_tool": "Instagram Downloader v1.0"
        }
    
    def download_posts(
        self,
        profile: instaloader.Profile,
        base_dir: Path,
        max_count: int = None
    ) -> dict:
        """Profil postlarını indir.
        
        Args:
            profile (instaloader.Profile): Profile object
            base_dir (Path): İndirme dizini
            max_count (int): Maximum post sayısı
            
        Returns:
            dict: İndirme istatistikleri
        """
        
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
        """Profil hikayelerini indir.
        
        Not: Instagram'ın kısıtlamaları nedeniyle, yalnızca profile owner'ın
        kendi hikayelerini arşiv olarak görebilmesi mümkündür.
        
        Args:
            profile (instaloader.Profile): Profile object
            base_dir (Path): İndirme dizini
            
        Returns:
            int: İndirilen story sayısı
        """
        
        downloaded_count = 0
        
        try:
            # Highlights listesini al (Instaloader 4.15+ API)
            highlights = self.loader.get_highlights(profile)
            
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
        """Metadata'yı JSON dosyasına kaydet.
        
        Args:
            base_dir (Path): Ana klasör yolu
            profile_metadata (dict): Profil metadata'sı
            download_stats (dict): İndirme istatistikleri
        """
        
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
        """Tüm profil indirme işlemini yönet.
        
        Args:
            username (str): Instagram profil adı
            max_posts (int): Maximum post sayısı
            download_stories (bool): Stories indirilsin mi
            download_highlights (bool): Highlights indirilsin mi
        """
        
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
        description="Instagram Herkese Açık Profil İndirici",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  %(prog)s cristiano
  %(prog)s cristiano -m 50
  %(prog)s cristiano -u myusername
  %(prog)s cristiano --no-stories
        """
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
        help="Konfigürasyon dosyası yolu (default: config.json)"
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
        logger.info("\nİndirme kullanıcı tarafından iptal edildi.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
