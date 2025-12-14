# 🌐 Instagram Downloader - Web Interface

## 📖 Genel Bakış

Modern, profesyonel ve kullanıcı dostu web arayüzü ile Instagram profil indirme aracı.

### ✨ Özellikler

- **🎯 Tek Profil İndirme**: Hızlı ve kolay profil indirme
- **👥 Toplu İndirme**: Birden fazla profili aynı anda indir
- **📊 Gerçek Zamanlı İlerleme**: Canlı download progress tracking
- **📁 İndirme Yönetimi**: İndirilen profilleri görüntüle ve ZIP olarak indir
- **🎨 Modern Tasarım**: Responsive, gradient ve glassmorphism tasarım
- **⚡ Hızlı ve Verimli**: Async işlemler ve threading
- **📱 Mobil Uyumlu**: Tüm cihazlarda mükemmel görünüm

## 🚀 Hızlı Başlangıç

### Gereksinimler

```bash
Python 3.8+
pip
```

### Kurulum

1. **Bağımlılıkları yükleyin:**

```bash
# Ana bağımlılıklar
pip install -r requirements.txt

# Web bağımlılıkları
pip install -r web/requirements.txt
```

2. **Web sunucusunu başlatın:**

```bash
python start_web.py
```

3. **Tarayıcınızı açın:**

```
http://localhost:5000
```

## 📂 Web Klasör Yapısı

```
web/
├── app.py                  # Flask backend
├── requirements.txt        # Web bağımlılıkları
├── templates/
│   └── index.html         # Ana sayfa
├── static/
│   ├── css/               # Custom CSS (optional)
│   ├── js/                # Custom JS (optional)
│   └── downloads/         # Geçici download dosyaları
└── README_WEB.md          # Bu dosya
```

## 🎯 Kullanım

### 1. Tek Profil İndirme

1. "Single Profile" sekmesini seçin
2. Instagram kullanıcı adını girin
3. (Opsiyonel) Maksimum post sayısı belirleyin
4. "Start Download" butonuna tıklayın
5. İlerlemeyi takip edin

### 2. Toplu İndirme

1. "Batch Download" sekmesini seçin
2. Her satıra bir kullanıcı adı yazın
3. (Opsiyonel) Maksimum post sayısı belirleyin
4. "Start Batch Download" butonuna tıklayın
5. Tüm indirmelerin ilerlemesini takip edin

### 3. İndirilen Dosyaları Yönetme

1. "My Downloads" sekmesini seçin
2. İndirilen profillerin listesini görün
3. "Download ZIP" ile profili ZIP olarak indirin

## 🔧 API Endpoints

### Download Endpoints

#### POST `/api/download/single`
Tek profil indir

**Body:**
```json
{
  "username": "cristiano",
  "max_posts": 10
}
```

**Response:**
```json
{
  "success": true,
  "job_id": "uuid",
  "message": "Download started"
}
```

#### POST `/api/download/batch`
Toplu indirme

**Body:**
```json
{
  "profiles": ["cristiano", "instagram"],
  "max_posts": 10
}
```

### Job Tracking

#### GET `/api/job/<job_id>`
Job durumunu sorgula

**Response:**
```json
{
  "job_id": "uuid",
  "status": "running",
  "progress": 45,
  "current_profile": "cristiano",
  "completed_profiles": [],
  "failed_profiles": []
}
```

#### GET `/api/jobs`
Tüm job'ları listele

### File Management

#### GET `/api/download/file/<filepath>`
Dosya veya klasörü indir (ZIP olarak)

#### GET `/api/profiles/list`
İndirilen profilleri listele

**Response:**
```json
[
  {
    "username": "cristiano",
    "photo_count": 50,
    "video_count": 20,
    "path": "downloads/cristiano"
  }
]
```

### Statistics

#### GET `/api/stats`
İstatistikleri getir

**Response:**
```json
{
  "total_jobs": 10,
  "completed_jobs": 8,
  "failed_jobs": 1,
  "running_jobs": 1,
  "successful_downloads": 15
}
```

#### GET `/health`
Health check

## 🎨 Tasarım Özellikleri

### Modern UI Bileşenleri

- **Gradient Backgrounds**: Purple-to-violet gradients
- **Glassmorphism**: Transparent, frosted glass cards
- **Smooth Animations**: Hover effects, transitions
- **Responsive Layout**: Mobile-first design
- **Icons**: Font Awesome 6 icons
- **Toast Notifications**: Real-time feedback

### Color Scheme

- Primary: Purple (#667eea, #764ba2)
- Success: Green
- Error: Red
- Info: Blue
- Warning: Yellow

## 🔒 Güvenlik

### Implemented Security

- ✅ Path traversal koruması
- ✅ File size limits (100MB)
- ✅ Input validation
- ✅ CORS headers (configure for production)
- ✅ Secure filename handling

### Production Önerileri

1. **Environment Variables**
```bash
export SECRET_KEY="your-secret-key-here"
export FLASK_ENV=production
```

2. **HTTPS Kullanın**
- SSL/TLS sertifikası ekleyin
- Nginx/Apache reverse proxy

3. **Rate Limiting**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
```

4. **Authentication** (Opsiyonel)
```python
from flask_login import LoginManager
# Kullanıcı girişi ekleyin
```

## 🚀 Production Deployment

### Option 1: Gunicorn (Önerilen)

```bash
# Gunicorn'u yükle
pip install gunicorn

# Uygulamayı başlat
cd web
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Option 2: Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Option 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN pip install -r web/requirements.txt

EXPOSE 5000

CMD ["python", "start_web.py"]
```

```bash
docker build -t instagram-downloader-web .
docker run -p 5000:5000 instagram-downloader-web
```

### Option 4: Cloud Platforms

#### Heroku
```bash
# Procfile
web: gunicorn web.app:app
```

#### AWS EC2
```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# Clone and setup
git clone your-repo
cd instagram_downloader
pip3 install -r requirements.txt
pip3 install -r web/requirements.txt

# Run with systemd
sudo systemctl start instagram-downloader
```

#### DigitalOcean App Platform
- Push to GitHub
- Connect repository
- Set start command: `python start_web.py`

## 📊 Performance

### Optimization Tips

1. **Caching**: Redis for job status
2. **Queue System**: Celery for background tasks
3. **Database**: PostgreSQL for job history
4. **CDN**: Serve static files from CDN
5. **Compression**: Enable gzip/brotli

### Scalability

```python
# Add Redis cache
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})

# Add Celery for tasks
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0')
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <pid> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Import Errors

```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Static Files Not Loading

```bash
# Check static folder permissions
chmod -R 755 web/static
```

## 📝 Customization

### Change Port

```python
# start_web.py
app.run(port=8080)  # Change to desired port
```

### Custom Logo

```html
<!-- templates/index.html -->
<img src="{{ url_for('static', filename='img/logo.png') }}" alt="Logo">
```

### Custom Styles

```css
/* static/css/custom.css */
.gradient-bg {
    background: linear-gradient(135deg, #your-color-1, #your-color-2);
}
```

## 📈 Monitoring

### Add Logging

```python
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
```

### Add Metrics

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
```

## 🤝 Contributing

Web arayüzü geliştirmelerine katkıda bulunmak için:

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - Ana projeyle aynı lisans

## ⚠️ Important Notes

### Legal & Ethical

- ✅ Sadece herkese açık profiller
- ❌ Private profiller yasak
- ⚠️ Instagram ToS'a uygunluk
- 🔒 Kişisel kullanım için

### Rate Limiting

- Instagram'ın rate limit'lerini aşmayın
- Profiller arası 3-5 saniye bekleyin
- Proxy kullanımını düşünün

### Data Privacy

- Kullanıcı verilerini saklamayın
- GDPR/KVKK'ya uyum
- Privacy policy ekleyin

## 🎉 Özellikler Yol Haritası

### v1.1 (Gelecek)
- [ ] User authentication
- [ ] Download history database
- [ ] Schedule downloads
- [ ] Email notifications
- [ ] API rate limiting

### v1.2
- [ ] Story downloading
- [ ] Highlights support
- [ ] Search functionality
- [ ] Dark mode
- [ ] Multi-language support

### v2.0
- [ ] Video processing (trim, compress)
- [ ] Automatic tagging
- [ ] Cloud storage integration
- [ ] Mobile app
- [ ] API documentation (Swagger)

## 📞 Support

- GitHub Issues: Bug reports
- Discussions: Feature requests
- Email: support@yourdomain.com

---

**Made with ❤️ for Instagram enthusiasts**

*Last updated: December 15, 2025*
