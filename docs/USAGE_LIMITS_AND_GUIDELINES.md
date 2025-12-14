# 📊 Instagram Downloader - Usage Limits & Guidelines

## 🚦 Rate Limits & Restrictions

### Instagram API Rate Limits

Instagram enforces various rate limits to prevent abuse and ensure service quality. Understanding these limits is crucial for successful downloads.

#### **Posts Per Profile**
- **Recommended:** 50 posts per download
- **Maximum (Safe):** 200 posts per session
- **Why:** Instagram throttles aggressive scraping. Staying under 200 posts reduces detection risk.

#### **Profiles Per Batch**
- **Recommended:** 5 profiles per batch
- **Maximum (Safe):** 10 profiles per batch
- **Why:** Batch downloads make multiple sequential requests. Too many profiles trigger rate limiting.

#### **Requests Per Hour**
- **Safe Zone:** ~200 requests/hour
- **Soft Limit:** ~500 requests/hour
- **Hard Limit:** ~1000 requests/hour (may trigger temporary IP ban)
- **Why:** Instagram monitors request patterns. Excessive requests appear bot-like.

#### **Delay Between Profiles**
- **Minimum:** 3 seconds
- **Recommended:** 5 seconds
- **Purpose:** Mimics human behavior, reduces detection

---

## 📋 Best Practices

### 1. **Start Small**
```
✅ Good:  Download 10-50 posts initially
❌ Bad:   Download 500+ posts immediately
```

### 2. **Use Reasonable Limits**
```python
# Recommended patterns
download_profile(username="cristiano", max_posts=50)   # ✅ Safe
download_profile(username="instagram", max_posts=100)  # ✅ Acceptable
download_profile(username="natgeo", max_posts=500)     # ⚠️ Risky
```

### 3. **Space Out Batch Downloads**
```python
# Good practice
batch_download([
    "user1",  # Wait 5 seconds
    "user2",  # Wait 5 seconds
    "user3"   # Wait 5 seconds
])

# Bad practice
batch_download([  # 20 profiles at once ❌
    "user1", "user2", ... "user20"
])
```

### 4. **Monitor Your Usage**
- Track failed requests
- Watch for error messages
- If you hit rate limits, wait 1-2 hours

---

## ⚖️ Legal & Ethical Guidelines

### ✅ Allowed Use Cases

1. **Personal Archiving**
   - Backing up your own content
   - Saving posts you're featured in (with permission)

2. **Educational Purposes**
   - Research projects
   - Academic studies
   - Learning web scraping techniques

3. **Non-Commercial Use**
   - Personal collections
   - Offline viewing
   - Content curation for personal reference

### ❌ Prohibited Use Cases

1. **Commercial Use**
   - Reselling downloaded content
   - Using content for advertising
   - Mass distribution for profit

2. **Privacy Violations**
   - Downloading private profiles (impossible anyway)
   - Sharing content without creator permission
   - Stalking or harassment

3. **Intellectual Property Theft**
   - Reposting without credit
   - Claiming ownership of others' work
   - Copyright infringement

4. **Platform Abuse**
   - Creating mirrors of Instagram
   - Automated mass scraping
   - Circumventing Instagram's access controls

---

## 🔒 Privacy & Security

### What We DO NOT Collect

- ❌ Passwords (no login required for public profiles)
- ❌ Personal information
- ❌ Cookies or tracking data
- ❌ User analytics beyond download counts

### What We DO Store

- ✅ Downloaded media files (local only)
- ✅ Metadata (public information)
- ✅ Session files (for authentication, if needed)

### Data Retention

- All downloads are stored **locally** on your device
- No cloud uploads or external storage
- You control all data - delete anytime

---

## 🛡️ Terms of Service Compliance

### Instagram Terms of Service

By using this tool, you agree to:

1. **Comply with Instagram ToS**
   - Link: https://help.instagram.com/581066165581870
   - You remain responsible for compliance

2. **Respect Community Guidelines**
   - Link: https://help.instagram.com/477434105621119
   - Don't use downloaded content to violate guidelines

3. **Honor Copyright & Trademarks**
   - Content belongs to original creators
   - Instagram logo/brand are Facebook/Meta trademarks

### Our Responsibilities

We provide the tool "as is" without warranty:
- ❌ No guarantee of uptime
- ❌ No warranty of functionality
- ❌ No liability for misuse
- ✅ Best-effort maintenance and updates

### User Responsibilities

Users are solely responsible for:
- ✅ Compliance with laws and regulations
- ✅ Respecting intellectual property rights
- ✅ Obtaining necessary permissions
- ✅ Not violating Instagram ToS
- ✅ Ethical use of downloaded content

---

## 🚨 Rate Limit Troubleshooting

### Signs You Hit Rate Limits

1. **Error Messages**
   ```
   "Too many requests"
   "Rate limit exceeded"
   "Login required" (for public profiles)
   "Connection refused"
   ```

2. **Symptoms**
   - Downloads suddenly failing
   - Slow response times
   - Incomplete downloads
   - HTTP 429 errors

### Solutions

#### Short-Term (Minutes)
1. **Wait 5-10 minutes**
   - Let Instagram's rate limiter reset
   - Try again with smaller limits

2. **Reduce Download Size**
   ```python
   # Instead of:
   download_profile("user", max_posts=500)
   
   # Try:
   download_profile("user", max_posts=50)
   ```

#### Medium-Term (Hours)
1. **Wait 1-2 hours**
   - Rate limits typically reset hourly
   - Check Instagram status page

2. **Use Different Network**
   - Switch WiFi networks
   - Use mobile data temporarily
   - Change VPN location (if using)

#### Long-Term (Prevention)
1. **Session Management**
   - Reuse session files
   - Don't create new sessions frequently

2. **Respect Limits**
   - Follow recommended limits
   - Add delays between requests
   - Use batch wisely

---

## 📈 Performance Optimization

### Maximize Download Success

#### 1. **Optimal Post Limits**
| Profile Size | Recommended Limit | Reason |
|--------------|-------------------|--------|
| Small (<100) | All posts | Complete archive |
| Medium (100-500) | 50-100 posts | Balance speed/quality |
| Large (500-5000) | 100-200 posts | Avoid rate limits |
| Huge (5000+) | Multiple batches | Split into sessions |

#### 2. **Batch Download Strategy**
```python
# Good: Small batches with delays
batch_1 = ["user1", "user2", "user3"]  # 3 profiles
wait(300)  # 5 minutes
batch_2 = ["user4", "user5", "user6"]  # Next 3

# Bad: Large batch, no delays
batch_huge = ["user1", ... "user20"]  # ❌ 20 at once
```

#### 3. **Time Your Downloads**
- **Best:** Off-peak hours (2 AM - 6 AM local time)
- **Good:** Weekday mornings
- **Avoid:** Weekend evenings (high Instagram traffic)

---

## 🔧 Technical Specifications

### System Requirements

#### Minimum
- Python 3.8+
- 2GB RAM
- 1GB free disk space
- Internet connection (5 Mbps)

#### Recommended
- Python 3.10+
- 4GB+ RAM
- 10GB+ free disk space
- Fast internet (25+ Mbps)

### Download Speeds

Typical speeds (varies by connection and Instagram throttling):

| Content Type | Avg Speed | Posts/Minute |
|--------------|-----------|--------------|
| Photos only | ~2 MB/s | 15-20 posts |
| Mixed content | ~1.5 MB/s | 10-15 posts |
| Videos only | ~1 MB/s | 5-10 posts |

### File Size Estimates

| Profile Type | Avg File Size | 100 Posts |
|--------------|---------------|-----------|
| Photo-heavy | 2-5 MB/post | 200-500 MB |
| Mixed | 5-10 MB/post | 500 MB-1 GB |
| Video-heavy | 10-50 MB/post | 1-5 GB |

---

## 📞 Support & Resources

### Getting Help

1. **Documentation**
   - [README.md](../README.md) - Quick start guide
   - [WEB_DEPLOYMENT.md](./WEB_DEPLOYMENT.md) - Deployment guide
   - [QUICKSTART.md](../QUICKSTART.md) - Basic usage

2. **Common Issues**
   - Rate limiting → Wait and retry
   - Private profiles → Not supported
   - Login errors → Check session file

3. **Best Practices**
   - Start with small downloads
   - Test with public profiles
   - Monitor error messages

### Reporting Issues

If you encounter problems:

1. **Check This Document First** - Most issues covered here
2. **Review Error Messages** - Often self-explanatory
3. **Test with Different Profile** - Isolate the issue
4. **Check Instagram Status** - May be their downtime

---

## 📜 Changelog & Updates

### Rate Limit Updates

Instagram periodically changes rate limits. We monitor and update:

- **Current limits** (as of Dec 2025): ~200-500 req/hour
- **Historical changes:** Documented in GitHub commits
- **Future updates:** Watch repository for announcements

### Tool Updates

We continuously improve the tool:

- Better rate limit handling
- Improved error messages
- Enhanced session management
- Performance optimizations

---

## 💡 Tips & Tricks

### Pro Tips

1. **Reuse Sessions**
   - Session files speed up downloads
   - Reduce login requests
   - Lower detection risk

2. **Progressive Downloads**
   ```python
   # Download in chunks
   download_profile("user", max_posts=50)   # Week 1
   download_profile("user", max_posts=100)  # Week 2
   # Cumulative archiving
   ```

3. **Peak vs Off-Peak**
   - Off-peak: Faster, fewer errors
   - Peak: Slower, higher chance of throttling

4. **Network Monitoring**
   ```bash
   # Monitor your requests
   watch -n 5 'curl -s localhost:5000/api/stats'
   ```

---

## 🎓 Educational Use

### Academic Research

If using for research:

1. **Cite Properly**
   ```
   Instagram Downloader (2025). Open-source tool for 
   Instagram content archiving. GitHub.
   ```

2. **Ethics Approval**
   - Get IRB approval if required
   - Follow institutional guidelines
   - Respect participant privacy

3. **Data Handling**
   - Anonymize when possible
   - Secure storage
   - Proper disposal after study

### Learning & Development

Great for learning:
- Web scraping techniques
- API rate limiting
- Python async programming
- Flask web development

---

## ⚠️ Important Reminders

### Final Warnings

1. **Respect Rate Limits** - Violating them may result in IP bans
2. **Stay Legal** - Comply with all applicable laws
3. **Be Ethical** - Respect privacy and intellectual property
4. **Use Responsibly** - Don't abuse the platform
5. **Stay Updated** - Instagram ToS and limits change

### Zero Tolerance

We do not support:
- ❌ Harassment or stalking
- ❌ Copyright infringement
- ❌ Commercial resale
- ❌ Privacy violations
- ❌ Terms of Service violations

---

**Last Updated:** December 15, 2025  
**Version:** 1.0.0  
**Status:** Active

For questions or updates, refer to the main [README.md](../README.md) or check the GitHub repository.
