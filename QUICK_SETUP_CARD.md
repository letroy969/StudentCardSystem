# Quick Setup Reference Card

Print this or keep it open while setting up!

---

## 📋 Environment Variables Checklist

Copy these into Render Dashboard → Environment:

```
✅ FLASK_ENV=production
✅ SECRET_KEY=<generate-random-64-char-hex>
✅ DATABASE_URL=<auto-set-when-database-linked>
✅ MAIL_SERVER=smtp.gmail.com
✅ MAIL_PORT=587
✅ MAIL_USE_TLS=True
✅ MAIL_USERNAME=umpdigitalcard@gmail.com
✅ MAIL_PASSWORD=<16-char-gmail-app-password>
✅ MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com
✅ SUPPORT_RECIPIENT=umpdigitalcard@gmail.com
⏳ PROFILE_BASE_URL=<set-after-first-deploy>
```

---

## 🔑 Where to Get Values

### Render PostgreSQL Database
1. Render Dashboard → PostgreSQL Database → Connect
2. **DATABASE_URL is auto-provided** when you link database to web service
3. No manual configuration needed!
4. Just link PostgreSQL database in web service settings

### Gmail App Password
1. [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
2. Select: Mail → Other → "Render Deployment"
3. Copy 16-character password (remove spaces)

### SECRET_KEY Generator
Run in terminal:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🚀 Render Disk Settings

**Name**: `uploads-disk`  
**Mount Path**: `/opt/render/project/src/static/uploads`  
**Size**: `1GB`

---

## ✅ Quick Test URLs

After deployment, test these:

1. Homepage: `https://your-app.onrender.com/`
2. Database: `https://your-app.onrender.com/test_db`
3. Register: `https://your-app.onrender.com/register`
4. Login: `https://your-app.onrender.com/login`

---

## 📚 Full Guide

See `STEP_BY_STEP_SETUP.md` for detailed instructions!

