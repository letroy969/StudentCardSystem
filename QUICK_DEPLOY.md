# Quick Deploy Guide for Render

Fast deployment guide - get your app live in 10 minutes!

## Prerequisites

- ✅ GitHub repository ready
- ✅ Render account (free tier available)
- ✅ Gmail App Password generated

## Step 1: Create PostgreSQL Database (2 min)

1. Go to [render.com](https://render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `student-card-db` (service name)
   - **Database**: `student_card_db` (database name)
   - **Plan**: **Free**
4. Click **"Create Database"**
5. Wait ~30 seconds

**Note**: 
- **Name** = What you see in Render dashboard
- **Database** = Actual database name (used in connection)
- **Deploy PostgreSQL Instance**: Render does this automatically - no need to select anything!

## Step 2: Initialize Database Schema (1 min)

1. Click your PostgreSQL database
2. Go to **"Connect"** → **"psql"**
3. Copy contents of `database_setup_postgresql.sql`
4. Paste and execute in psql console
5. Should see `CREATE TABLE` messages

## Step 3: Create Web Service (3 min)

1. Render Dashboard → **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `letroy969/StudentCardSystem`
3. Configure:
   - **Name**: `ump-digital-card`
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `gunicorn app:app`
   - **Datadog API Key**: Leave empty (optional - not needed)
4. **Link PostgreSQL Database** (important!)
   - Scroll to "Add-ons" → Link your PostgreSQL database
   - This auto-sets `DATABASE_URL`!

## Step 4: Set Environment Variables (2 min)

In Render Dashboard → Environment, add:

```
FLASK_ENV=production
SECRET_KEY=<generate: python -c "import secrets; print(secrets.token_hex(32))">
DATABASE_URL=<auto-set-when-database-linked>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalcard@gmail.com
MAIL_PASSWORD=<your-16-char-gmail-app-password>
MAIL_DEFAULT_SENDER=umpdigitalcard@gmail.com
SUPPORT_RECIPIENT=umpdigitalcard@gmail.com
```

**Note**: `DATABASE_URL` is automatically set when you link the database!

## Step 5: Deploy (2 min)

1. Click **"Create Web Service"**
2. Wait for build (5-10 minutes)
3. Copy your app URL: `https://your-app.onrender.com`

## Step 6: Set PROFILE_BASE_URL (1 min)

After first deploy:

1. Environment → Add Variable
2. Key: `PROFILE_BASE_URL`
3. Value: `https://your-app.onrender.com` (your actual URL)
4. Save (triggers redeploy)

## Step 7: Add Render Disk (CRITICAL!)

**Without this, files are lost on redeploy!**

1. Settings → Disks → Add Disk
2. Name: `uploads-disk`
3. Mount: `/opt/render/project/src/static/uploads`
4. Size: `1GB`
5. Add Disk → Redeploy

## Step 8: Test

Visit these URLs:
- Homepage: `https://your-app.onrender.com/`
- Database: `https://your-app.onrender.com/test_db`
- Should show: "Database connected! Current time: ..."

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database fails | Link PostgreSQL database to web service |
| Email not sending | Verify Gmail App Password (16 chars) |
| QR codes wrong URL | Set `PROFILE_BASE_URL` env var |
| Files lost | Add Render Disk (Step 7) |

## Full Guide

See `STEP_BY_STEP_SETUP.md` for detailed instructions.

---

**That's it!** Your app is live! 🚀
