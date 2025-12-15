# 🚀 Önizleme Sorunu - Hızlı Çözüm

## Problem
Önizlemede görseller görünmüyor çünkü Instagram artık çoğu profil için giriş yapılmasını gerektiriyor.

## ✅ KALICI ÇÖZÜM

### Adım 1: Instagram Hesabıyla Giriş Yap

Terminal'de şu komutu çalıştır:

```powershell
python login.py
```

Kullanıcı adı ve şifrenizi girin. Session dosyası oluşturulacak.

### Adım 2: Web Sunucusunu Yeniden Başlat

```powershell
python web/app.py
```

### Adım 3: Önizlemeyi Test Et

http://localhost:5000 adresine git ve herhangi bir kullanıcı adı ile önizleme yap.

## 🔒 Güvenlik Notu

- Şifreniz sadece Instagram'a gönderilir, hiçbir yerde saklanmaz
- Sadece `session.pickle` dosyası oluşturulur (bu da şifreli)
- Session dosyasını `.gitignore`'a ekledik

## 🎯 Test Kullanıcıları

Giriş yaptıktan sonra şu kullanıcılarla test edebilirsiniz:
- `cristiano` - 600M+ takipçi
- `nasa` - Uzay fotoğrafları
- `natgeo` - National Geographic

## ⚡ Hızlı Komutlar

```powershell
# Login
python login.py

# Server başlat
python web/app.py

# Test et
start http://localhost:5000
```

## 🐛 Sorun Devam Ederse

1. Session dosyasını sil: `Remove-Item session.pickle`
2. Tekrar login ol: `python login.py`
3. Server'ı yeniden başlat

---

**Not:** Instagram rate limit koyabilir. Eğer "rate limit" hatası alırsanız birkaç dakika bekleyin.
