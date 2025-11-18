# Render Quick Start Guide

Quick reference for deploying to Render.

## Prerequisites Checklist

- [ ] GitHub repository connected
- [ ] PlanetScale database created
- [ ] Gmail App Password generated
- [ ] Render account created

## 1. Environment Variables (Copy-Paste Ready)

Add these in Render Dashboard → Environment:

```bash
FLASK_ENV=production
SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_hex(32))">
DB_HOST=<your-planetscale-host>.psdb.cloud
DB_PORT=3306
DB_NAME=student_card_db
DB_USER=<planetscale-username>
DB_PASSWORD=<planetscale-password>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalcard@gmail.com
MAIL_PASSWORD=<16-char-gmail-app-password>
MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com
SUPPORT_RECIPIENT=umpdigitalcard@gmail.com
```

**After first deploy**, add:
```bash
PROFILE_BASE_URL=https://your-app-name.onrender.com
```

## 2. Render Service Configuration

- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Python Version**: 3.11.9 (auto-detected from runtime.txt)

## 3. Add Render Disk (For File Persistence)

1. Settings → Disks → Add Disk
2. Name: `uploads-disk`
3. Mount Path: `/opt/render/project/src/static/uploads`
4. Size: `1GB`

## 4. Test Deployment

Visit these URLs after deployment:

- Homepage: `https://your-app.onrender.com`
- Database Test: `https://your-app.onrender.com/test_db`
- Should show: "Database connected! Current time: ..."

## Common Issues

| Issue | Solution |
|-------|----------|
| Database connection fails | Check PlanetScale credentials, ensure DB_HOST includes `.psdb.cloud` |
| Email not sending | Verify Gmail App Password (16 chars, no spaces) |
| QR codes wrong URL | Set `PROFILE_BASE_URL` env var |
| Files lost on redeploy | Add Render Disk (see step 3) |

## Full Documentation

See `DEPLOYMENT.md` for complete step-by-step guide.

