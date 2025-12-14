# 🔐 Instagram Downloader - Güvenlik Rehberi

Bu dokümantasyon, projenin güvenlik özelliklerini ve en iyi pratikleri açıklar.

---

## ⚠️ Hassas Bilgilerin Korunması

### 1. Kimlik Bilgileri

**❌ ASLA YAPMAYIN:**
```bash
# Şifreyi komut satırında yazmayın (terminal geçmişinde kalır!)
python run_downloader.py user -u myusername -p mypassword123

# Şifreyi config.json'a yazmayın
# Şifreyi kaynak koduna yazmayın
```

**✅ DOĞRU YÖNTEMLER:**

#### Yöntem 1: İnteraktif Şifre Girişi (Önerilen)
```bash
python run_downloader.py cristiano -u myusername
# Program şifre soracaktır ve ekranda görünmeyecektir
```

#### Yöntem 2: Environment Variables
```bash
# .env dosyası oluşturun (Git'e eklenmeyecek)
cp .env.example .env

# .env dosyasını düzenleyin
INSTAGRAM_USERNAME=myusername
INSTAGRAM_PASSWORD=mypassword
```

```python
# Kodunuzda kullanın
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('INSTAGRAM_USERNAME')
password = os.getenv('INSTAGRAM_PASSWORD')
```

#### Yöntem 3: Session Yönetimi
```python
# İlk giriş
session_mgr.login("username", "password")  # Session kaydedilir

# Sonraki kullanımlarda şifre gerektirmez
session_mgr.load_session()  # Kayıtlı session kullanılır
```

---

## 🔒 .gitignore Koruması

Projedeki `.gitignore` dosyası hassas verileri otomatik olarak korur:

```gitignore
# Kimlik bilgileri ve session
session.pickle
*.pickle
.env
config.json

# İndirilen içerik (GDPR/DMCA koruması)
downloads/
*.mp4
*.jpg
*.jpeg
*.png
```

### Kontrol Etme

Git'e eklenmemesi gereken dosyaları kontrol edin:

```bash
# Hangi dosyalar Git'e eklenmiş?
git ls-files | grep -E "(config.json|.env|session.pickle)"

# Sonuç boş olmalı! Eğer dosya görünüyorsa:
git rm --cached config.json
git rm --cached .env
git commit -m "Remove sensitive files"
```

---

## 🛡️ Web Interface Güvenliği

### Secret Key Yönetimi

**❌ Güvensiz:**
```python
app.config['SECRET_KEY'] = 'hardcoded-secret-key'
```

**✅ Güvenli:**
```python
# web/app.py
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
```

**Üretim ortamında:**
```bash
# .env dosyasına ekleyin
SECRET_KEY=$(python -c "import os; print(os.urandom(24).hex())")
echo "SECRET_KEY=$SECRET_KEY" >> .env
```

### HTTPS Kullanımı

Üretim ortamında HTTPS zorunlu:

```python
# Nginx veya Apache ile SSL sertifikası kullanın
# Let's Encrypt ücretsiz SSL sağlar
```

---

## 📋 Güvenlik Kontrol Listesi

Projeyi GitHub'a yüklemeden önce:

- [ ] `config.json` Git'e eklenmemiş
- [ ] `.env` dosyası Git'e eklenmemiş
- [ ] `session.pickle` Git'e eklenmemiş
- [ ] Kaynak kodda hardcoded şifre yok
- [ ] README.md'de örnek şifreler gerçek değil
- [ ] `SECRET_KEY` environment variable'dan okunuyor
- [ ] `.gitignore` dosyası doğru yapılandırılmış
- [ ] `config.json.example` hassas bilgi içermiyor

### Otomatik Kontrol

```bash
# Hassas bilgi arama
grep -r "password.*=.*\"" --exclude-dir=.git --exclude="*.md"
grep -r "token.*=.*\"" --exclude-dir=.git --exclude="*.md"
grep -r "api_key.*=.*\"" --exclude-dir=.git --exclude="*.md"

# Sonuç: "No matches found" olmalı
```

---

## 🚨 Güvenlik İhlali Durumunda

Eğer yanlışlıkla hassas bilgi commit edilmişse:

### 1. Git History'den Temizleme

```bash
# Dosyayı tamamen history'den kaldır
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch config.json' \
  --prune-empty --tag-name-filter cat -- --all

# Zorunlu push (dikkatli kullanın!)
git push origin --force --all
```

### 2. Şifre/Token Değiştirme

- Instagram şifrenizi derhal değiştirin
- GitHub Personal Access Token'ı iptal edin
- API key'leri yenileyin

### 3. GitHub'dan Destek

Hassas bilgi public repository'de görünüyorsa:
- GitHub Support'a başvurun: https://support.github.com/
- Cache'i temizlemelerini isteyin

---

## 🔐 Ek Güvenlik Önlemleri

### Rate Limiting

```python
# Web interface'de DDoS koruması
from flask_limiter import Limiter

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/api/download')
@limiter.limit("10 per minute")
def download():
    pass
```

### Input Validation

```python
# Kullanıcı girişlerini her zaman doğrulayın
import re

def is_valid_username(username):
    return re.match(r'^[a-zA-Z0-9._]{1,30}$', username) is not None

if not is_valid_username(user_input):
    raise ValueError("Invalid username format")
```

### Logging (Hassas Bilgi İçermeden)

```python
# ❌ Şifre loglama
logger.info(f"Login: {username}:{password}")

# ✅ Güvenli loglama
logger.info(f"Login attempt: {username}")
```

---

## 📚 Kaynaklar

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [Python Security Guidelines](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [Instagram API Terms of Service](https://www.instagram.com/about/legal/terms/api/)

---

## 📧 Güvenlik Sorunları

Güvenlik açığı bulursanız:

1. **Public issue açMAYIN** (açığı ifşa etmez)
2. GitHub'da "Security" → "Report a vulnerability" kullanın
3. Veya doğrudan iletişime geçin: [GitHub Profile](https://github.com/Xtra01)

**Responsible Disclosure Policy:** 90 gün içinde yanıt verilir.

---

> ⚠️ **Yasal Uyarı:** Bu araç yalnızca kendi hesabınız veya izin aldığınız hesaplar için kullanılmalıdır. Instagram Terms of Service'i ihlal etmekten sorumlu değiliz.
