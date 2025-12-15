# 🚀 GitHub'a Yükleme Rehberi

Bu dosya projenizi GitHub'a nasıl yükleyeceğinizi adım adım anlatır.

## 📋 Ön Hazırlık

### 1. Git Kurulu mu Kontrol Edin

```powershell
git --version
```

Eğer kurulu değilse: https://git-scm.com/download/win

### 2. Git Config (İlk kullanım için)

```powershell
git config --global user.name "Xtra01"
git config --global user.email "your-email@example.com"
```

## 🔧 GitHub Repository Oluşturma

### 1. GitHub'da Yeni Repo Oluştur

1. https://github.com/Xtra01 adresine git
2. "New repository" tıkla
3. **Repository name:** `instagram_downloader`
4. **Description:** "Modern Instagram content downloader with web interface"
5. **Public** seç
6. ❌ **Initialize this repository with a README** seçme (zaten var)
7. "Create repository" tıkla

## 📤 Projeyi GitHub'a Yükle

### Seçenek 1: Yeni Repository (Önerilen)

```powershell
# Projenin klasörüne git
cd D:\CodeProjects\instagram_downloader

# Git başlat
git init

# Tüm dosyaları ekle (.gitignore otomatik çalışır)
git add .

# İlk commit
git commit -m "Initial commit: Instagram Downloader v1.1.0 with web interface and URL support"

# Ana branch'i main olarak ayarla
git branch -M main

# Remote ekle (kendi repo URL'inizi kullanın)
git remote add origin https://github.com/Xtra01/instagram_downloader.git

# Push et
git push -u origin main
```

### Seçenek 2: Eğer Repo Zaten Varsa

```powershell
cd D:\CodeProjects\instagram_downloader

# Mevcut remote'u kontrol et
git remote -v

# Eğer farklı ise, değiştir
git remote set-url origin https://github.com/Xtra01/instagram_downloader.git

# Son değişiklikleri ekle
git add .
git commit -m "Update: Add web interface, URL support, and comprehensive documentation"

# Push
git push -u origin main
```

## 🔐 Personal Access Token (PAT) ile Push

Eğer parola sorarsa (GitHub artık şifre kabul etmiyor):

### 1. PAT Oluştur

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token (classic)
4. Scopes: `repo` seç
5. Generate token
6. **Token'ı kopyala** (bir daha göremezsin!)

### 2. Token ile Push

```powershell
# Push ederken username sorarsa: Xtra01
# Password sorarsa: TOKEN'I YAPIŞTIR (şifre değil!)

git push -u origin main
```

veya

```powershell
# Direkt token ile
git remote set-url origin https://YOUR_TOKEN@github.com/Xtra01/instagram_downloader.git
git push -u origin main
```

## 🎯 İlk Push Sonrası Kontrol

### 1. GitHub'da Kontrol Et

https://github.com/Xtra01/instagram_downloader adresine git ve şunları kontrol et:

- ✅ README.md düzgün görünüyor mu?
- ✅ LICENSE dosyası var mı?
- ✅ Klasör yapısı doğru mu?
- ✅ .gitignore çalıştı mı? (downloads klasörü yok olmalı)

### 2. Repository Settings

**GitHub'da Settings sekmesinde:**

1. **About** bölümüne açıklama ekle:
   ```
   🔮 Modern Instagram content downloader with web interface. 
   Download profiles, posts, reels & IGTV with URL support.
   ```

2. **Topics** ekle:
   ```
   instagram, instagram-downloader, instagram-scraper, 
   python, flask, web-interface, instaloader, 
   instagram-api, instagram-bot, downloader
   ```

3. **Website** ekle:
   ```
   https://github.com/Xtra01/instagram_downloader#readme
   ```

## 📝 Gelecekteki Güncellemeler

### Yeni değişiklik yaptıktan sonra:

```powershell
# Değişiklikleri ekle
git add .

# Commit (açıklayıcı mesaj yaz)
git commit -m "feat: Add story download support"

# Push
git push
```

### Commit Mesaj Örnekleri:

```bash
git commit -m "feat: Add new feature"           # Yeni özellik
git commit -m "fix: Fix bug in progress bar"    # Bug fix
git commit -m "docs: Update README"             # Dokümantasyon
git commit -m "refactor: Improve code structure" # Kod iyileştirme
git commit -m "style: Format code"              # Kod formatı
git commit -m "test: Add tests"                 # Test ekleme
```

## 🌟 Repository'yi Güzelleştir

### 1. README.md Banner/Logo Ekle (Opsiyonel)

Canva veya Figma'da bir banner yap, sonra:

```powershell
# Projeye ekle
mkdir docs/images
# Banner'ı docs/images/banner.png olarak kaydet

# Commit
git add docs/images/banner.png
git commit -m "docs: Add banner image"
git push
```

README.md'de kullan:
```markdown
![Banner](docs/images/banner.png)
```

### 2. Badges Ekle (Zaten ekli!)

README'de şunlar var:
- MIT License badge
- Python version badge
- GitHub stars badge

### 3. Screenshot Ekle

Web arayüzünden screenshot al:

```powershell
# Screenshot'u kaydet
mkdir docs/images
# docs/images/screenshot.png olarak kaydet

git add docs/images/screenshot.png
git commit -m "docs: Add web interface screenshot"
git push
```

## 🎉 Tamamlandı!

Projeniz artık GitHub'da! 

**Repository URL:**
```
https://github.com/Xtra01/instagram_downloader
```

## 📊 GitHub Actions (İleri Seviye - Opsiyonel)

CI/CD için GitHub Actions eklemek isterseniz:

```yaml
# .github/workflows/python-app.yml oluştur
name: Python Application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## 🔄 Branch Stratejisi (Ekip Çalışması İçin)

```powershell
# Development branch
git checkout -b develop
git push -u origin develop

# Feature branch
git checkout -b feature/new-feature
# ... değişiklikler yap ...
git commit -m "feat: Add new feature"
git push -u origin feature/new-feature
# GitHub'da Pull Request aç
```

## 🆘 Sorun Giderme

### "Permission denied" hatası

```powershell
# SSH key ekle veya PAT kullan (yukarıda anlatıldı)
```

### "fatal: not a git repository"

```powershell
git init
```

### Large files hatası (>100MB)

```powershell
# Git LFS kullan veya dosyayı .gitignore'a ekle
echo "large-file.zip" >> .gitignore
```

### Commit history temizle (gerekirse)

```powershell
# DİKKAT: Bu tehlikelidir, yedek al!
git checkout --orphan new-main
git add .
git commit -m "Initial commit"
git branch -D main
git branch -m main
git push -f origin main
```

---

**Hazır mısınız? Yukarıdaki komutları çalıştırın! 🚀**
