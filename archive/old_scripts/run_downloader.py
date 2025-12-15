#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Ana Giriş Noktası
Root dizininden çalıştırılabilir wrapper script
"""

import sys
from pathlib import Path

# src klasörünü path'e ekle
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# main modülünü import et ve çalıştır
from main import main

if __name__ == "__main__":
    main()
