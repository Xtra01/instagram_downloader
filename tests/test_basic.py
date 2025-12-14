#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Temel Test Dosyası
Unit tests ve integration tests

Kullanım:
    python test_basic.py
    pytest test_basic.py -v
"""

import sys
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# src klasörünü path'e ekle
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Modülleri import et
try:
    from main import (
        InstagramDownloaderConfig,
        SessionManager,
        InstagramProfileDownloader
    )
    from advanced import RateLimiter, ExponentialBackoffRetry, InstagramAPIWrapper
except ImportError as e:
    print(f"Hata: Gerekli modüller yüklenemiyor: {e}")
    sys.exit(1)


class TestInstagramDownloaderConfig(unittest.TestCase):
    """Config sınıfı için test"""
    
    def test_default_config(self):
        """Default konfigürasyon değerlerini test et"""
        config = InstagramDownloaderConfig()
        
        # Varsayılan değerleri kontrol et
        self.assertEqual(config.get("base_download_dir"), "downloads")
        self.assertIsInstance(config.get("min_delay_between_requests"), (int, float))
        self.assertGreaterEqual(config.get("min_delay_between_requests"), 1)
    
    def test_config_get_default(self):
        """get() metodunun default değerlerini test et"""
        config = InstagramDownloaderConfig()
        
        # Var olmayan key için default değer
        result = config.get("nonexistent_key", "default_value")
        self.assertEqual(result, "default_value")


class TestRateLimiter(unittest.TestCase):
    """RateLimiter sınıfı için test"""
    
    def test_initialization(self):
        """RateLimiter başlatmayı test et"""
        limiter = RateLimiter(min_delay=2.0, max_delay=60.0)
        
        self.assertEqual(limiter.min_delay, 2.0)
        self.assertEqual(limiter.max_delay, 60.0)
        self.assertIsNone(limiter.last_request_time)
    
    def test_wait_if_needed_first_call(self):
        """İlk çağrıda bekleme olmamalı"""
        limiter = RateLimiter(min_delay=2.0)
        
        import time
        start = time.time()
        limiter.wait_if_needed()
        elapsed = time.time() - start
        
        # İlk çağrı minimal bekleme yapmalı
        self.assertLess(elapsed, 0.1)
    
    def test_wait_if_needed_subsequent_call(self):
        """Ardışık çağrıda min_delay kadar beklemeli"""
        limiter = RateLimiter(min_delay=1.0)
        
        import time
        limiter.wait_if_needed()  # İlk çağrı
        
        start = time.time()
        limiter.wait_if_needed()  # İkinci çağrı
        elapsed = time.time() - start
        
        # En az min_delay kadar beklemiş olmalı (jitter hariç)
        self.assertGreaterEqual(elapsed, 0.8)


class TestExponentialBackoffRetry(unittest.TestCase):
    """ExponentialBackoffRetry sınıfı için test"""
    
    def test_initialization(self):
        """ExponentialBackoffRetry başlatmayı test et"""
        retry = ExponentialBackoffRetry(max_retries=3, base_delay=1.0)
        
        self.assertEqual(retry.max_retries, 3)
        self.assertEqual(retry.base_delay, 1.0)
    
    def test_successful_execution(self):
        """Başarılı fonksiyon yürütmesini test et"""
        retry_handler = ExponentialBackoffRetry(max_retries=3)
        
        @retry_handler.retry
        def successful_function():
            return "success"
        
        result = successful_function()
        self.assertEqual(result, "success")
    
    def test_retry_on_failure(self):
        """Hata durumunda retry mekanizmasını test et"""
        retry_handler = ExponentialBackoffRetry(max_retries=3, base_delay=0.1)
        
        call_count = [0]
        
        @retry_handler.retry
        def failing_function():
            call_count[0] += 1
            if call_count[0] < 3:
                raise ConnectionError("Test error")
            return "success after retries"
        
        result = failing_function()
        
        # 3 kez deneme yapılmış olmalı
        self.assertEqual(call_count[0], 3)
        self.assertEqual(result, "success after retries")
    
    def test_max_retries_exceeded(self):
        """Max retry aşıldığında exception fırlatmalı"""
        retry_handler = ExponentialBackoffRetry(max_retries=2, base_delay=0.1)
        
        @retry_handler.retry
        def always_failing_function():
            raise ValueError("Always fails")
        
        # Max retry aşıldığında exception fırlatmalı
        with self.assertRaises(ValueError):
            always_failing_function()


class TestSessionManager(unittest.TestCase):
    """SessionManager sınıfı için test"""
    
    def test_initialization(self):
        """SessionManager başlatmayı test et"""
        session_mgr = SessionManager("test_session.pickle")
        
        # session_file string olarak saklanıyor, Path değil
        self.assertEqual(session_mgr.session_file, "test_session.pickle")
    
    def test_load_or_create(self):
        """Session yükleme veya oluşturmayı test et"""
        session_mgr = SessionManager("test_session.pickle")
        loader = session_mgr.load_or_create()
        
        # Loader objesi oluşturulmuş olmalı
        self.assertIsNotNone(loader)
        
        # Cleanup
        if Path("test_session.pickle").exists():
            Path("test_session.pickle").unlink()


class TestInstagramProfileDownloader(unittest.TestCase):
    """InstagramProfileDownloader sınıfı için test"""
    
    @patch('main.instaloader.Instaloader')
    def test_initialization(self, mock_loader_class):
        """Downloader başlatmayı test et"""
        mock_loader = Mock()
        config = InstagramDownloaderConfig()
        
        downloader = InstagramProfileDownloader(mock_loader, config)
        
        self.assertEqual(downloader.loader, mock_loader)
        self.assertEqual(downloader.config, config)
    
    @patch('main.instaloader.Profile')
    def test_get_profile_public(self, mock_profile_class):
        """Public profil çekmeyi test et"""
        mock_loader = Mock()
        mock_profile = Mock()
        mock_profile.username = "testuser"
        mock_profile.is_private = False
        
        # Profile.from_username metodunu mock'la
        mock_profile_class.from_username.return_value = mock_profile
        
        config = InstagramDownloaderConfig()
        downloader = InstagramProfileDownloader(mock_loader, config)
        
        profile = downloader.get_profile("testuser")
        
        self.assertIsNotNone(profile)
        self.assertEqual(profile.username, "testuser")


class TestInstagramAPIWrapper(unittest.TestCase):
    """InstagramAPIWrapper sınıfı için test"""
    
    def test_initialization(self):
        """API Wrapper başlatmayı test et"""
        mock_loader = Mock()
        wrapper = InstagramAPIWrapper(mock_loader, min_delay=1.0, max_retries=3)
        
        self.assertEqual(wrapper.loader, mock_loader)
        self.assertIsNotNone(wrapper.rate_limiter)
        self.assertIsNotNone(wrapper.retry_handler)


class TestIntegration(unittest.TestCase):
    """Integration testleri"""
    
    def test_end_to_end_config_flow(self):
        """Config -> SessionManager -> Downloader akışını test et"""
        # Config oluştur
        config = InstagramDownloaderConfig()
        
        # SessionManager oluştur
        session_mgr = SessionManager("test_integration_session.pickle")
        loader = session_mgr.load_or_create()
        
        # Downloader oluştur
        downloader = InstagramProfileDownloader(loader, config)
        
        # Tüm objeler oluşturulmuş olmalı
        self.assertIsNotNone(config)
        self.assertIsNotNone(session_mgr)
        self.assertIsNotNone(loader)
        self.assertIsNotNone(downloader)
        
        # Cleanup
        if Path("test_integration_session.pickle").exists():
            Path("test_integration_session.pickle").unlink()


def run_tests():
    """Tüm testleri çalıştır"""
    print("\n" + "=" * 60)
    print("Instagram Downloader - Test Suite")
    print("=" * 60 + "\n")
    
    # Test suite oluştur
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Tüm test sınıflarını ekle
    suite.addTests(loader.loadTestsFromTestCase(TestInstagramDownloaderConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestRateLimiter))
    suite.addTests(loader.loadTestsFromTestCase(TestExponentialBackoffRetry))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestInstagramProfileDownloader))
    suite.addTests(loader.loadTestsFromTestCase(TestInstagramAPIWrapper))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Testleri çalıştır
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Sonuçları yazdır
    print("\n" + "=" * 60)
    print("Test Sonuçları:")
    print(f"Toplam: {result.testsRun}")
    print(f"Başarılı: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Başarısız: {len(result.failures)}")
    print(f"Hata: {len(result.errors)}")
    print("=" * 60 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
