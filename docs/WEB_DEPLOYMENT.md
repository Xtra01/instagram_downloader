# 🚀 Instagram Downloader - Web Deployment Guide

## 📋 Production Deployment Checklist

### ✅ Pre-Deployment

- [ ] Test all features locally
- [ ] Review security settings
- [ ] Configure environment variables
- [ ] Set up error logging
- [ ] Prepare database (if using)
- [ ] Configure rate limiting
- [ ] Set up monitoring

### 🔧 Environment Setup

#### 1. Environment Variables

Create `.env` file:

```bash
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=production
FLASK_DEBUG=0

# Application Settings
MAX_WORKERS=4
PORT=5000
HOST=0.0.0.0

# Instagram Settings
MAX_POSTS_PER_PROFILE=50
DOWNLOAD_TIMEOUT=300
RATE_LIMIT_DELAY=3

# File Storage
UPLOAD_FOLDER=/var/www/uploads
DOWNLOAD_FOLDER=/var/www/downloads
MAX_FILE_SIZE=104857600  # 100MB

# Optional: Database
DATABASE_URL=postgresql://user:pass@localhost/instagram_downloader

# Optional: Redis Cache
REDIS_URL=redis://localhost:6379/0

# Optional: Email Notifications
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### 2. Load Environment Variables

Update `web/app.py`:

```python
from dotenv import load_dotenv
load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 104857600))
```

### 🌐 Deployment Options

## Option 1: Gunicorn + Nginx (Recommended)

### Step 1: Install Gunicorn

```bash
pip install gunicorn
```

### Step 2: Create Gunicorn Config

Create `gunicorn_config.py`:

```python
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2
max_requests = 1000
max_requests_jitter = 50

# Logging
accesslog = "/var/log/instagram-downloader/access.log"
errorlog = "/var/log/instagram-downloader/error.log"
loglevel = "info"

# Process naming
proc_name = "instagram-downloader"

# Server mechanics
daemon = False
pidfile = "/var/run/instagram-downloader.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = "/tmp"
```

### Step 3: Run with Gunicorn

```bash
gunicorn -c gunicorn_config.py web.app:app
```

### Step 4: Nginx Configuration

Create `/etc/nginx/sites-available/instagram-downloader`:

```nginx
upstream instagram_downloader {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    # Client body size
    client_max_body_size 100M;
    
    # Static files
    location /static {
        alias /var/www/instagram-downloader/web/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    
    # Downloads
    location /downloads {
        alias /var/www/downloads;
        internal;
    }
    
    # Proxy to Flask
    location / {
        proxy_pass http://instagram_downloader;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # WebSocket support (for future)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
    
    # Health check
    location /health {
        proxy_pass http://instagram_downloader;
        access_log off;
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/instagram-downloader /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: Systemd Service

Create `/etc/systemd/system/instagram-downloader.service`:

```ini
[Unit]
Description=Instagram Downloader Web Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/instagram-downloader
Environment="PATH=/var/www/instagram-downloader/venv/bin"
ExecStart=/var/www/instagram-downloader/venv/bin/gunicorn \
    -c gunicorn_config.py \
    web.app:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable instagram-downloader
sudo systemctl start instagram-downloader
sudo systemctl status instagram-downloader
```

## Option 2: Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY web/requirements.txt web/
COPY src/requirements.txt src/ || true

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r web/requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copy application
COPY . .

# Create necessary directories
RUN mkdir -p /app/downloads /app/web/static/downloads

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')"

# Run with gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "web.app:app"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./downloads:/app/downloads
      - ./logs:/app/logs
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - FLASK_ENV=production
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped
    networks:
      - instagram-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - instagram-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/nginx/ssl
      - ./web/static:/usr/share/nginx/html/static:ro
    depends_on:
      - web
    restart: unless-stopped
    networks:
      - instagram-network

volumes:
  redis-data:

networks:
  instagram-network:
    driver: bridge
```

Deploy:

```bash
docker-compose up -d
docker-compose logs -f
```

## Option 3: Cloud Platforms

### Heroku

1. **Create Procfile:**

```
web: gunicorn -c gunicorn_config.py web.app:app
```

2. **Deploy:**

```bash
heroku create your-app-name
git push heroku main
heroku ps:scale web=1
heroku open
```

### AWS Elastic Beanstalk

1. **Install EB CLI:**

```bash
pip install awsebcli
```

2. **Initialize:**

```bash
eb init -p python-3.11 instagram-downloader
eb create instagram-downloader-env
eb open
```

### DigitalOcean App Platform

1. Push to GitHub
2. Connect repository
3. Configure:
   - Build Command: `pip install -r requirements.txt && pip install -r web/requirements.txt`
   - Run Command: `python start_web.py`
   - Port: 5000

### Google Cloud Run

1. **Build container:**

```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/instagram-downloader
```

2. **Deploy:**

```bash
gcloud run deploy instagram-downloader \
    --image gcr.io/PROJECT_ID/instagram-downloader \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --timeout 300
```

## 🔒 Security Hardening

### 1. Rate Limiting

Install Flask-Limiter:

```bash
pip install Flask-Limiter
```

Add to `app.py`:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="redis://localhost:6379"
)

@app.route('/api/download/single', methods=['POST'])
@limiter.limit("10 per minute")
def download_single():
    # ... existing code
```

### 2. CORS Configuration

```bash
pip install Flask-CORS
```

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://your-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 3. Input Validation

```python
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class DownloadForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(),
        Length(min=1, max=30)
    ])
    max_posts = IntegerField('max_posts', validators=[
        NumberRange(min=1, max=100)
    ])
```

### 4. Authentication (Optional)

```bash
pip install Flask-Login
```

```python
from flask_login import LoginManager, login_required

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/api/download/single', methods=['POST'])
@login_required
def download_single():
    # ... existing code
```

## 📊 Monitoring & Logging

### 1. Application Monitoring

```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

### 2. Performance Monitoring

```bash
pip install prometheus-flask-exporter
```

```python
from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='1.0.0')
```

### 3. Structured Logging

```python
import logging
from logging.handlers import RotatingFileHandler
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName
        }
        return json.dumps(log_data)

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
handler.setFormatter(JsonFormatter())
app.logger.addHandler(handler)
```

## 🧪 Testing in Production

### Health Check

```bash
curl https://your-domain.com/health
```

Expected response:

```json
{
  "status": "healthy",
  "timestamp": "2025-12-15T01:00:00",
  "version": "1.0.0"
}
```

### Load Testing

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Test
ab -n 1000 -c 10 https://your-domain.com/
```

### Smoke Tests

```bash
# Test single download
curl -X POST https://your-domain.com/api/download/single \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "max_posts": 1}'

# Test job status
curl https://your-domain.com/api/jobs

# Test stats
curl https://your-domain.com/api/stats
```

## 📈 Performance Optimization

### 1. Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    'CACHE_DEFAULT_TIMEOUT': 300
})

@app.route('/api/profiles/list')
@cache.cached(timeout=60)
def list_profiles():
    # ... existing code
```

### 2. Async Tasks with Celery

```bash
pip install celery redis
```

```python
from celery import Celery

celery = Celery(
    app.name,
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def download_profile_async(username, max_posts):
    # Download logic
    pass
```

### 3. Database for Job History

```bash
pip install Flask-SQLAlchemy
```

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    # ... more fields
```

## 🔄 Backup & Recovery

### Backup Script

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/instagram-downloader"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup downloads
tar -czf "$BACKUP_DIR/downloads_$DATE.tar.gz" /var/www/downloads

# Backup database (if using)
pg_dump instagram_downloader > "$BACKUP_DIR/db_$DATE.sql"

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

Add to crontab:

```bash
0 2 * * * /path/to/backup.sh
```

## 📞 Support & Maintenance

### Monitoring Commands

```bash
# Check service status
sudo systemctl status instagram-downloader

# View logs
sudo journalctl -u instagram-downloader -f

# Check Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check application logs
tail -f /var/www/instagram-downloader/logs/app.log

# Monitor resources
htop
```

### Common Issues

**Issue: High memory usage**
```bash
# Increase worker memory limit in gunicorn_config.py
max_requests = 500  # Restart worker after N requests
```

**Issue: Slow downloads**
```bash
# Increase timeout in nginx.conf
proxy_read_timeout 600s;
```

**Issue: SSL certificate expired**
```bash
# Renew Let's Encrypt certificate
sudo certbot renew
sudo systemctl reload nginx
```

## ✅ Post-Deployment Checklist

- [ ] SSL certificate installed and working
- [ ] Domain pointing to server
- [ ] Firewall configured (only 80, 443 open)
- [ ] Automatic backups scheduled
- [ ] Monitoring alerts configured
- [ ] Rate limiting active
- [ ] Error tracking enabled
- [ ] Health checks passing
- [ ] Load testing completed
- [ ] Documentation updated

## 🎉 Success!

Your Instagram Downloader web application is now live and production-ready!

---

**Need help?** Contact support or open an issue on GitHub.

*Last updated: December 15, 2025*
