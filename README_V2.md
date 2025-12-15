# Instagram Downloader v2.0 🔥

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/Xtra01/instagram_downloader?style=social)](https://github.com/Xtra01/instagram_downloader)
[![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)](https://github.com/Xtra01/instagram_downloader/releases)

> **Professional Instagram downloader with saveclip.app feature parity**

Complete rewrite with modern web interface, profile picture downloads, stories support, and **100% accurate media counting**. Download photos, videos, reels, stories, profile pictures, and entire profiles.

![Web Interface Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Modern+Web+Interface)

---

## 🎯 What's New in v2.0

### ✨ Major Features Added
- **📸 Profile Picture Downloads** - HD quality profile pictures
- **🕒 Stories Support** - Download active stories (requires login)
- **🎬 Highlights** - Save all highlights permanently  
- **🔢 Accurate Counting** - Real file-based media counting (fixed 0 count bug)
- **🎨 Modern UI** - Completely redesigned interface inspired by saveclip.app
- **⚡ Quick Actions** - One-click buttons for content type selection
- **📊 Better Progress Tracking** - Real-time updates with phase indicators

### 🐛 Fixed Issues
- ❌ **FIXED**: Downloaded files showing as 0 photos/videos
- ❌ **FIXED**: Profile picture not downloading
- ❌ **FIXED**: Story downloads not working  
- ❌ **FIXED**: Single URL downloads failing
- ❌ **FIXED**: Progress bar not updating
- ❌ **FIXED**: Max posts limit not respected

---

## ✨ Features

### 🌐 Modern Web Interface
- **Beautiful Design**: Gradient backgrounds, card-based layout, responsive
- **Quick Action Buttons**: Profile, Profile Pic, Stories, Post/Reel, Auto-detect
- **Real-time Progress**: Live download tracking with accurate counters
- **My Downloads Section**: Visual grid with photo/video counts and ZIP downloads
- **Mobile Responsive**: Perfect experience on all devices

### 📥 Download Capabilities

| Content Type | Supported | Description |
|-------------|-----------|-------------|
| 📸 **Profile Pictures** | ✅ | HD quality profile picture |
| 🕒 **Stories** | ✅ | Active stories (requires login) |
| 🎬 **Highlights** | ✅ | All saved highlights |
| 📷 **Posts** | ✅ | Photo posts and carousels |
| 🎥 **Reels** | ✅ | Short-form videos |
| 📺 **IGTV** | ✅ | Long-form videos |
| 👤 **Full Profile** | ✅ | Complete profile backup |
| 📦 **Batch** | ✅ | Multiple profiles at once |

### 🎯 Smart Features
- **Auto URL Detection**: Paste any Instagram link, automatic type detection
- **Flexible Limits**: Control max posts, include/exclude specific content
- **Accurate Counting**: Real `.jpg`, `.mp4` file counting - no more 0 files bug!
- **ZIP Export**: One-click download of entire profile as ZIP
- **Error Recovery**: Graceful handling of failed downloads
- **Session Management**: Persistent login state

---

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/Xtra01/instagram_downloader.git
cd instagram_downloader

# Install dependencies
pip install -r requirements.txt

# Start web interface
python web/app.py
```

Open browser: **http://localhost:5000**

---

## 💻 Usage

### Web Interface (Recommended)

1. **Open** http://localhost:5000
2. **Select** content type (Profile, Profile Pic, Stories, Post, or Auto)
3. **Paste** Instagram URL or username:
   - `cristiano` → Download profile
   - `https://instagram.com/p/ABC123/` → Download post
   - `https://instagram.com/reel/XYZ789/` → Download reel
4. **Configure** options (max posts, include profile pic, etc.)
5. **Click** "Start Download"
6. **Download** ZIP from "My Downloads" section

### Command Line Interface

```bash
# Download profile (50 posts)
python run_downloader.py cristiano -m 50

# Download with login (for stories/highlights)
python run_downloader.py cristiano -u your_username

# Batch download
python run_batch.py profiles.txt
```

---

## 📋 Supported URL Formats

```
✅ Profile:        https://instagram.com/cristiano
✅ Profile:        cristiano
✅ Post:           https://instagram.com/p/ABC123/
✅ Reel:           https://instagram.com/reel/XYZ789/
✅ IGTV:           https://instagram.com/tv/DEF456/
✅ Story:          https://instagram.com/stories/user/123/ (requires login)
```

---

## 🏗️ Project Structure

```
instagram_downloader/
├── web/                    # Web application
│   ├── app.py             # Flask backend (v2.0)
│   ├── templates/
│   │   └── index.html     # Modern UI (v2.0)
│   └── static/            # Static assets
├── core/                   # Core downloader module (NEW)
│   ├── downloader.py      # Enhanced download functions
│   └── __init__.py
├── src/                    # Original source files
│   ├── main.py            # Config, session management
│   ├── advanced.py        # Advanced features
│   └── batch_download.py  # Batch processing
├── archive/                # Old versions backup
├── docs/                   # Documentation
├── downloads/              # Downloaded content
└── requirements.txt        # Python dependencies
```

---

## 🔧 Configuration

### .env File (Optional)

```bash
# .env
SECRET_KEY=your-secret-key-here
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
```

### Download Options

```python
# In web interface or via API
{
    "url": "cristiano",
    "type": "profile",           # profile, profile_pic, story, post, reel, igtv
    "max_posts": 50,              # Limit posts (1-500)
    "download_profile_pic": true, # Include profile picture
    "download_stories": false,    # Include stories (requires login)
    "download_highlights": false  # Include highlights (requires login)
}
```

---

## 📊 API Endpoints

### POST `/api/download`
Download Instagram content

```json
{
    "url": "https://instagram.com/p/ABC123/",
    "type": "auto",
    "max_posts": 50
}
```

### GET `/api/job/<job_id>`
Get download status

```json
{
    "job_id": "uuid",
    "status": "completed",
    "progress": 100,
    "downloaded_items": 42,
    "total_items": 42
}
```

### GET `/api/profiles/list`
List downloaded profiles with accurate counts

```json
[
    {
        "username": "cristiano",
        "photo_count": 35,
        "video_count": 15,
        "total_count": 50,
        "path": "downloads/cristiano"
    }
]
```

### GET `/api/download/zip/<folder>`
Download profile as ZIP

---

## 🎨 Screenshots

### Main Interface
![Main Interface](https://via.placeholder.com/600x400/667eea/ffffff?text=Main+Download+Interface)

### Active Downloads
![Active Downloads](https://via.placeholder.com/600x300/764ba2/ffffff?text=Real-time+Progress)

### My Downloads
![My Downloads](https://via.placeholder.com/600x400/667eea/ffffff?text=Downloaded+Content)

---

## 🐛 Troubleshooting

### Issue: Downloaded files show as "0 Photos / 0 Videos"
**Status**: ✅ **FIXED in v2.0**

Old versions had incorrect counting. v2.0 uses real file-based counting:
```python
counts = downloader.count_downloaded_media(download_dir)
# Counts actual .jpg, .mp4 files, not folder estimates
```

### Issue: Profile picture not downloading
**Status**: ✅ **FIXED in v2.0**

Now available via:
- Quick Action button "Profile Pic"
- Or enable "Include Profile Picture" in profile downloads

### Issue: Stories not downloading
**Status**: ✅ **FIXED in v2.0**

Stories require login:
```bash
python run_downloader.py username -u your_username
# Web: Enable "Include Stories" checkbox
```

### Issue: Single URL downloads fail
**Status**: ✅ **FIXED in v2.0**

Enhanced URL parsing now supports all formats. Test at http://localhost:5000/health

---

## 📚 Documentation

- [Security Guide](SECURITY.md) - Best practices and safety
- [Quick Start with URLs](QUICKSTART_URL_SUPPORT.md) - URL usage examples
- [GitHub Upload Guide](GITHUB_UPLOAD_GUIDE.md) - Git/GitHub tutorial

---

## ⚠️ Important Notice

### Legal & Ethical Use
- ✅ **For personal use only**
- ✅ Download your own content or public profiles
- ✅ Respect Instagram Terms of Service
- ✅ Respect intellectual property rights
- ❌ **Do not** download private content without permission
- ❌ **Do not** use for commercial purposes
- ❌ **Do not** redistribute downloaded content

### Rate Limits
- **Posts per profile**: Recommended 50, max 200
- **Profiles per batch**: Recommended 5, max 10  
- **Requests per hour**: ~200 safe limit
- **Delay between profiles**: 3-5 seconds minimum

Instagram may throttle or block excessive requests. Use responsibly!

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📜 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file.

```
MIT License - Copyright (c) 2025 Xtra01 (https://github.com/Xtra01)
```

---

## 🙏 Acknowledgments

- [Instaloader](https://instaloader.github.io/) - Core Instagram API library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Tailwind CSS](https://tailwindcss.com/) - UI styling
- [Font Awesome](https://fontawesome.com/) - Icons
- Inspired by [saveclip.app](https://saveclip.app/en) design

---

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/Xtra01/instagram_downloader/issues)
- **Security**: See [SECURITY.md](SECURITY.md) for reporting vulnerabilities
- **GitHub**: [@Xtra01](https://github.com/Xtra01)

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

[![Star History](https://api.star-history.com/svg?repos=Xtra01/instagram_downloader&type=Date)](https://star-history.com/#Xtra01/instagram_downloader&Date)

---

## 📈 Changelog

### v2.0.0 (2025-12-15)
- ✨ **NEW**: Profile picture HD downloads
- ✨ **NEW**: Stories and highlights support
- ✨ **NEW**: Modern web interface redesign
- ✨ **NEW**: Quick action buttons
- ✨ **NEW**: Accurate file-based media counting
- 🐛 **FIX**: 0 photos/videos display bug
- 🐛 **FIX**: Single URL download failures
- 🐛 **FIX**: Progress bar not updating
- 🐛 **FIX**: Max posts limit not respected
- 📁 **REFACTOR**: Modular core/downloader.py
- 📁 **CLEANUP**: Archived unused files
- 🔒 **SECURITY**: Enhanced SECRET_KEY handling

### v1.1.0 (2025-12-14)
- Initial URL parsing support
- Basic web interface
- Profile downloads

---

<div align="center">

**Made with ❤️ by [Xtra01](https://github.com/Xtra01)**

⭐ Star this repo if you find it useful!

[Report Bug](https://github.com/Xtra01/instagram_downloader/issues) · [Request Feature](https://github.com/Xtra01/instagram_downloader/issues)

</div>
