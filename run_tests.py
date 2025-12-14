#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Instagram Downloader - Test Giriş Noktası
Root dizininden çalıştırılabilir wrapper script
"""

import sys
from pathlib import Path

# tests klasörünü path'e ekle
tests_path = Path(__file__).parent / "tests"
sys.path.insert(0, str(tests_path))

# src klasörünü de path'e ekle (test_basic'in import etmesi için)
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# test_basic modülünü import et ve çalıştır
from test_basic import run_tests

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
