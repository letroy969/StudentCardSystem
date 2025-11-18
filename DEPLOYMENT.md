# Render Deployment Guide

Complete guide to deploy the UMP Digital Card system on Render with all functionalities working.

## Prerequisites

- GitHub repository with your code
- PlanetScale account (free tier available)
- Gmail account with App Password enabled
- Render account (free tier available)

---

## Step 1: Database Setup (PlanetScale)

### 1.1 Create PlanetScale Database

1. Go to [planetscale.com](https://planetscale.com/) and sign up/login
2. Click **"Create database"**
3. Name: `student_card_db`
4. Region: Choose closest to your users
5. Plan: **Free** (sufficient for development)
6. Click **"Create database"**

### 1.2 Import Database Schema

**Option A: Using PlanetScale CLI (Recommended)**
```bash
# Install PlanetScale CLI
# Windows: Download from https://github.com/planetscale/cli/releases
# Mac: brew install planetscale/tap/pscale
# Linux: See https://github.com/planetscale/cli

# Login
pscale auth login

# Connect to your database
pscale connect student_card_db main --port 3306

# In another terminal, import schema
mysql -h 127.0.0.1 -P 3306 -u root -p < database_setup.sql
```

**Option B: Using PlanetScale Dashboard**
1. Go to your database → **"Console"**
2. Copy contents of `database_setup.sql`
3. Paste and execute in the SQL console

### 1.3 Get Database Credentials

1. Go to your database → **"Settings"** → **"Passwords"**
2. Click **"Create password"**
3. Name: `render-production`
4. Copy these values (you'll need them):
   - **Host**: `xxxxx.us-east-2.psdb.cloud`
   - **Username**: `xxxxx`
   - **Password**: `pscale_pw_xxxxx`
   - **Database**: `student_card_db`
   - **Port**: `3306`

---

## Step 2: Gmail App Password Setup

### 2.1 Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already enabled

### 2.2 Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Name: `Render Deployment`
5. Click **Generate**
6. **Copy the 16-character password** (you'll need this)

---

## Step 3: Render Deployment

### 3.1 Create Web Service

1. Go to [render.com](https://render.com/) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select the repository: `letroy969/UniOne-Digital-ID` (or your repo)
5. Click **"Connect"**

### 3.2 Configure Service

**Basic Settings:**
- **Name**: `ump-digital-card` (or your preferred name)
- **Region**: Choose closest to your users
- **Branch**: `main` (or your main branch)
- **Root Directory**: Leave empty (or `card1` if your app is in a subdirectory)

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (deploys on every push to main branch)

### 3.3 Set Environment Variables

Go to **"Environment"** tab and add these variables:

#### Required Variables

```bash
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=<generate-a-random-string-here>
# Use: python -c "import secrets; print(secrets.token_hex(32))"

# Database Configuration (from PlanetScale)
DB_HOST=<your-planetscale-host>.us-east-2.psdb.cloud
DB_PORT=3306
DB_NAME=student_card_db
DB_USER=<your-planetscale-username>
DB_PASSWORD=<your-planetscale-password>

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalcard@gmail.com
MAIL_PASSWORD=<your-gmail-app-password-16-chars>
MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com
SUPPORT_RECIPIENT=umpdigitalcard@gmail.com
```

#### Optional Variables

```bash
# Profile Base URL (set after first deploy)
PROFILE_BASE_URL=https://your-app-name.onrender.com
```

**Important Notes:**
- Replace `<...>` placeholders with actual values
- `SECRET_KEY`: Generate using: `python -c "import secrets; print(secrets.token_hex(32))"`
- `PROFILE_BASE_URL`: Set this **after** first deployment (you'll get the URL from Render)

### 3.4 Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (5-10 minutes)
3. Check **"Logs"** tab for any errors
4. Once deployed, you'll get a URL like: `https://your-app-name.onrender.com`

### 3.5 Set PROFILE_BASE_URL

After first successful deployment:

1. Copy your Render app URL (e.g., `https://your-app-name.onrender.com`)
2. Go to **"Environment"** tab
3. Add/Update: `PROFILE_BASE_URL=https://your-app-name.onrender.com`
4. Click **"Save Changes"** (will trigger auto-redeploy)

---

## Step 4: File Upload Persistence (CRITICAL)

**⚠️ IMPORTANT**: Render's filesystem is ephemeral. Uploaded files will be lost on redeploy unless you add persistent storage.

### Option 1: Render Disk (Recommended for Testing)

1. Go to your Render service → **"Settings"**
2. Scroll to **"Disks"** section
3. Click **"Add Disk"**
4. Configure:
   - **Name**: `uploads-disk`
   - **Mount Path**: `/opt/render/project/src/static/uploads`
   - **Size**: `1GB` (free tier allows this)
5. Click **"Add Disk"**
6. Redeploy your service

**Note**: The mount path must match where your app saves files. Check `app.py` line 88: `UPLOAD_FOLDER = 'static/uploads'`

### Option 2: Cloud Storage (Recommended for Production)

For production, consider using:
- **AWS S3** (most reliable)
- **Cloudinary** (easy integration)
- **Google Cloud Storage**

This requires code changes to upload directly to cloud storage instead of local filesystem.

---

## Step 5: Verify Deployment

### 5.1 Test Basic Functionality

1. **Homepage**: Visit your Render URL
   - Should load without errors

2. **Database Connection**: Visit `https://your-app.onrender.com/test_db`
   - Should show: "Database connected! Current time: ..."

3. **Registration**: Try registering a test account
   - Email must end with `@ump.ac.za`
   - Should redirect to login page

4. **Login**: Login with test account
   - Should redirect to dashboard

### 5.2 Test Core Features

- ✅ **Student Card Creation**: Upload photo, fill form, submit
- ✅ **QR Code Generation**: Check if QR code appears on card preview
- ✅ **Public Profile**: Scan QR code or visit `/profile/<email>`
- ✅ **File Uploads**: Upload photo and PDF (if Render Disk added)
- ✅ **Email Notifications**: Submit support ticket, check email

### 5.3 Common Issues & Solutions

#### Issue: Database Connection Failed
**Solution**: 
- Verify PlanetScale credentials are correct
- Check PlanetScale database is active
- Ensure `DB_HOST` includes `.psdb.cloud` domain

#### Issue: Email Not Sending
**Solution**:
- Verify Gmail App Password is correct (16 characters, no spaces)
- Check `MAIL_USERNAME` matches the Gmail account
- Ensure 2FA is enabled on Gmail account

#### Issue: QR Codes Point to Wrong URL
**Solution**:
- Set `PROFILE_BASE_URL` environment variable
- Ensure it matches your Render app URL exactly
- Redeploy after setting

#### Issue: Files Lost on Redeploy
**Solution**:
- Add Render Disk (see Step 4)
- Or implement cloud storage (S3, Cloudinary, etc.)

#### Issue: OpenCV Build Fails
**Solution**:
- Render should handle this automatically
- If issues persist, check Python version (should be 3.11.9)
- Verify `opencv-python` is in requirements.txt

---

## Step 6: Production Checklist

Before going live, verify:

- [ ] All environment variables set correctly
- [ ] Database schema imported successfully
- [ ] Test registration/login works
- [ ] QR codes generate correctly
- [ ] Public profiles accessible
- [ ] File uploads work (if Render Disk added)
- [ ] Email notifications work
- [ ] Support ticket submission works
- [ ] Reports page loads (if accessible)
- [ ] HTTPS enabled (Render does this automatically)
- [ ] Custom domain configured (optional)

---

## Step 7: Monitoring & Maintenance

### 7.1 Monitor Logs

- Go to Render Dashboard → Your Service → **"Logs"**
- Watch for errors, especially:
  - Database connection issues
  - Email sending failures
  - File upload errors

### 7.2 Database Backups

- PlanetScale free tier includes automatic backups
- Check PlanetScale dashboard → **"Backups"** tab

### 7.3 Update Deployment

- Push changes to GitHub main branch
- Render will auto-deploy (if enabled)
- Or manually trigger deploy from Render dashboard

---

## Environment Variables Reference

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `FLASK_ENV` | Yes | Flask environment | `production` |
| `SECRET_KEY` | Yes | Flask secret key | Random 64-char hex |
| `DB_HOST` | Yes | Database host | `xxx.psdb.cloud` |
| `DB_PORT` | Yes | Database port | `3306` |
| `DB_NAME` | Yes | Database name | `student_card_db` |
| `DB_USER` | Yes | Database username | `xxxxx` |
| `DB_PASSWORD` | Yes | Database password | `pscale_pw_xxx` |
| `MAIL_SERVER` | Yes | SMTP server | `smtp.gmail.com` |
| `MAIL_PORT` | Yes | SMTP port | `587` |
| `MAIL_USE_TLS` | Yes | Use TLS | `True` |
| `MAIL_USERNAME` | Yes | Email username | `your@email.com` |
| `MAIL_PASSWORD` | Yes | Email app password | `16-char-password` |
| `MAIL_DEFAULT_SENDER` | Yes | Default sender | `your@email.com` |
| `SUPPORT_RECIPIENT` | Yes | Support email | `support@email.com` |
| `PROFILE_BASE_URL` | No | Base URL for QR codes | `https://app.onrender.com` |

---

## Support

If you encounter issues:

1. Check Render logs: Dashboard → Service → Logs
2. Check PlanetScale logs: Dashboard → Database → Logs
3. Verify all environment variables are set correctly
4. Test database connection: `/test_db` endpoint
5. Review this guide for common issues

---

## Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. ✅ Set up monitoring/alerts
3. ✅ Configure custom domain (optional)
4. ✅ Set up automated backups
5. ✅ Document any custom configurations

**Happy Deploying! 🚀**

