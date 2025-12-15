#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Toplu (Batch) İndirme Script'i
Birden fazla profili otomatik olarak indir

Kullanım:
    python batch_download.py profiles.txt
    python batch_download.py profiles.txt -m 20 -u myusername
    
profiles.txt formatı:
    cristiano
    instagram
    natgeo
    # yorum satırı
"""

import sys
import os
import argparse
import logging
import time
from pathlib import Path
from typing import List, Optional

# Parent directory'yi path'e ekle
sys.path.insert(0, str(Path(__file__).parent))

try:
    from main import (
        InstagramDownloaderConfig,
        SessionManager,
        InstagramProfileDownloader
    )
    from instaloader.exceptions import (
        ProfileNotExistsException,
        PrivateProfileNotFollowedException,
        LoginRequiredException
    )
except ImportError as e:
    print(f"Hata: Gerekli modüller yüklenemiyor: {e}")
    print("Kurulum: pip install -r requirements.txt")
    sys.exit(1)

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchDownloader:
    """Toplu profil indirme yöneticisi"""
    
    def __init__(
        self,
        downloader: InstagramProfileDownloader,
        max_posts: Optional[int] = None,
        download_stories: bool = True,
        delay_between_profiles: float = 5.0
    ):
        """
        Args:
            downloader: InstagramProfileDownloader instance
            max_posts: Her profil için max post sayısı
            download_stories: Stories indirilsin mi?
            delay_between_profiles: Profiller arası bekleme süresi (saniye)
        """
        self.downloader = downloader
        self.max_posts = max_posts
        self.download_stories = download_stories
        self.delay_between_profiles = delay_between_profiles
        
        # İstatistikler
        self.stats = {
            'total': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'profiles': []
        }
    
    def read_profiles_from_file(self, file_path: str) -> List[str]:
        """
        Profil listesini dosyadan oku
        
        Args:
            file_path: Profil listesi dosyası yolu
            
        Returns:
            List[str]: Profil kullanıcı adları listesi
        """
        profiles = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Boş satırları ve yorumları atla
                    if not line or line.startswith('#'):
                        continue
                    
                    # Virgül veya boşlukla ayrılmış listeler için
                    if ',' in line:
                        profiles.extend([p.strip() for p in line.split(',') if p.strip()])
                    elif ' ' in line:
                        profiles.extend([p.strip() for p in line.split() if p.strip()])
                    else:
                        profiles.append(line)
            
            logger.info(f"{len(profiles)} profil dosyadan okundu: {file_path}")
            return profiles
            
        except FileNotFoundError:
            logger.error(f"Dosya bulunamadı: {file_path}")
            return []
        except Exception as e:
            logger.error(f"Dosya okuma hatası: {e}")
            return []
    
    def download_profile(self, username: str) -> bool:
        """
        Tek bir profili indir
        
        Args:
            username: Profil kullanıcı adı
            
        Returns:
            bool: Başarılı ise True
        """
        logger.info(f"\n{'=' * 60}")
        logger.info(f"İndiriliyor: {username}")
        logger.info(f"{'=' * 60}")
        
        try:
            self.downloader.download_profile(
                username=username,
                max_posts=self.max_posts,
                download_stories=self.download_stories,
                download_highlights=True
            )
            
            self.stats['successful'] += 1
            self.stats['profiles'].append({
                'username': username,
                'status': 'success'
            })
            
            logger.info(f"✅ Başarılı: {username}")
            return True
            
        except ProfileNotExistsException:
            logger.warning(f"❌ Profil bulunamadı: {username}")
            self.stats['failed'] += 1
            self.stats['profiles'].append({
                'username': username,
                'status': 'not_found'
            })
            return False
            
        except PrivateProfileNotFollowedException:
            logger.warning(f"⚠️ Profil özel: {username}")
            self.stats['skipped'] += 1
            self.stats['profiles'].append({
                'username': username,
                'status': 'private'
            })
            return False
            
        except Exception as e:
            logger.error(f"❌ Hata ({username}): {type(e).__name__}: {e}")
            self.stats['failed'] += 1
            self.stats['profiles'].append({
                'username': username,
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def download_batch(self, profiles: List[str]) -> dict:
        """
        Toplu profil indirme
        
        Args:
            profiles: Profil kullanıcı adları listesi
            
        Returns:
            dict: İstatistikler
        """
        self.stats['total'] = len(profiles)
        
        logger.info(f"\n{'=' * 60}")
        logger.info(f"Toplu İndirme Başlıyor")
        logger.info(f"Toplam Profil: {len(profiles)}")
        logger.info(f"{'=' * 60}\n")
        
        for i, username in enumerate(profiles, 1):
            logger.info(f"\n[{i}/{len(profiles)}] İşleniyor: {username}")
            
            # Profili indir
            self.download_profile(username)
            
            # Son profil değilse bekle
            if i < len(profiles):
                logger.info(f"Sonraki profil için {self.delay_between_profiles}s bekleniyor...")
                time.sleep(self.delay_between_profiles)
        
        # Özet rapor
        self.print_summary()
        
        return self.stats
    
    def print_summary(self):
        """Özet raporu yazdır"""
        logger.info(f"\n{'=' * 60}")
        logger.info("TOPLU İNDİRME ÖZET RAPORU")
        logger.info(f"{'=' * 60}")
        logger.info(f"Toplam Profil:    {self.stats['total']}")
        logger.info(f"✅ Başarılı:      {self.stats['successful']}")
        logger.info(f"❌ Başarısız:     {self.stats['failed']}")
        logger.info(f"⚠️ Atlandı:       {self.stats['skipped']}")
        logger.info(f"{'=' * 60}")
        
        # Detaylı liste
        if self.stats['profiles']:
            logger.info("\nDetaylı Sonuçlar:")
            for profile in self.stats['profiles']:
                status_emoji = {
                    'success': '✅',
                    'not_found': '❌',
                    'private': '⚠️',
                    'error': '❌'
                }.get(profile['status'], '?')
                
                logger.info(f"  {status_emoji} {profile['username']}: {profile['status']}")
        
        logger.info(f"\n{'=' * 60}\n")


def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(
        description="Instagram Toplu Profil İndirici",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  %(prog)s profiles.txt
  %(prog)s profiles.txt -m 20
  %(prog)s profiles.txt -u myusername --no-stories
  %(prog)s profiles.txt --delay 10
        """
    )
    
    parser.add_argument(
        "profiles_file",
        help="Profil listesi dosyası (her satırda bir kullanıcı adı)"
    )
    
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
        help="Her profil için maximum indirilecek post sayısı"
    )
    
    parser.add_argument(
        "--no-stories",
        action="store_true",
        help="Stories indirmeyi devre dışı bırak"
    )
    
    parser.add_argument(
        "--delay",
        type=float,
        default=5.0,
        help="Profiller arası bekleme süresi (saniye, default: 5.0)"
    )
    
    parser.add_argument(
        "-c", "--config",
        default="config.json",
        help="Konfigürasyon dosyası yolu (default: config.json)"
    )
    
    args = parser.parse_args()
    
    # Profil listesini kontrol et
    if not Path(args.profiles_file).exists():
        logger.error(f"Profil listesi dosyası bulunamadı: {args.profiles_file}")
        logger.info("\nÖrnek profiles.txt formatı:")
        logger.info("  cristiano")
        logger.info("  instagram")
        logger.info("  natgeo")
        logger.info("  # yorum satırı")
        sys.exit(1)
    
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
    
    # Batch Downloader'ı başlat
    batch = BatchDownloader(
        downloader=downloader,
        max_posts=args.max_posts,
        download_stories=not args.no_stories,
        delay_between_profiles=args.delay
    )
    
    # Profilleri oku
    profiles = batch.read_profiles_from_file(args.profiles_file)
    
    if not profiles:
        logger.error("İndirilecek profil bulunamadı.")
        sys.exit(1)
    
    # Toplu indirme başlat
    try:
        stats = batch.download_batch(profiles)
        
        # Çıkış kodu belirle
        exit_code = 0 if stats['failed'] == 0 else 1
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        logger.info("\n\nToplu indirme kullanıcı tarafından iptal edildi.")
        batch.print_summary()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
