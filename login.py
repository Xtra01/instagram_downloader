#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Login Script - Quick Login Tool
Creates session for preview system
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.main import SessionManager
import getpass

def main():
    print("=" * 60)
    print("Instagram Downloader - Login Tool")
    print("=" * 60)
    print()
    
    username = input("Instagram kullanıcı adınız: ").strip()
    password = getpass.getpass("Instagram şifreniz (görünmez): ")
    
    if not username or not password:
        print("❌ Kullanıcı adı ve şifre gerekli!")
        sys.exit(1)
    
    print()
    print("🔄 Instagram'a giriş yapılıyor...")
    
    session_manager = SessionManager()
    loader = session_manager.load_or_create()
    
    try:
        success = session_manager.login(username, password)
        
        if success:
            print("✅ Giriş başarılı!")
            print(f"📁 Session kaydedildi: {session_manager.session_file}")
            print()
            print("Artık web arayüzünde önizleme yapabilirsiniz!")
            print("Sunucuyu başlatmak için: python web/app.py")
        else:
            print("❌ Giriş başarısız!")
            print("Kullanıcı adı ve şifrenizi kontrol edin.")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
