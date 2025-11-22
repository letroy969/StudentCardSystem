# Railway MySQL Quick Start Guide

Quick reference for setting up Railway MySQL database for your Student Card System.

---

## 🚀 5-Minute Setup

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (free)

### Step 2: Create MySQL Database
1. Click **"New Project"**
2. Click **"New"** → **"Database"** → **"Add MySQL"**
3. Wait ~30 seconds for setup

### Step 3: Get Credentials
1. Click on MySQL database
2. Go to **"Variables"** tab
3. Copy these values:
   - `MYSQLHOST` → `DB_HOST` in Render
   - `MYSQLPORT` → `DB_PORT` in Render (usually 3306)
   - `MYSQLDATABASE` → `DB_NAME` in Render
   - `MYSQLUSER` → `DB_USER` in Render
   - `MYSQLPASSWORD` → `DB_PASSWORD` in Render

### Step 4: Import Schema
1. Click MySQL database → **"Data"** tab
2. Click **"Open MySQL Console"** or **"Query"**
3. Copy contents of `database_setup.sql`
4. Paste and run in Railway SQL console

### Step 5: Use in Render
Copy Railway credentials to Render environment variables (see below)

---

## 📋 Render Environment Variables

Set these in Render Dashboard → Environment:

```
DB_HOST=<MYSQLHOST-value-from-railway>
DB_PORT=3306
DB_NAME=<MYSQLDATABASE-value-from-railway>
DB_USER=<MYSQLUSER-value-from-railway>
DB_PASSWORD=<MYSQLPASSWORD-value-from-railway>
```

**Example:**
```
DB_HOST=containers-us-west-123.railway.app
DB_PORT=3306
DB_NAME=railway
DB_USER=root
DB_PASSWORD=abc123xyz
```

---

## ✅ Verify Setup

1. Deploy on Render
2. Visit: `https://your-app.onrender.com/test_db`
3. Should see: `"Database connected! Current time: ..."`

---

## 💰 Railway Free Tier

- **$5 credit/month** (usually enough for small apps)
- **512MB RAM** per database
- **1GB storage** per database
- **No sleep** - databases stay active 24/7

---

## 🔧 Troubleshooting

### Database Connection Fails
- Check Railway database is running (should show "Active")
- Verify credentials match Railway Variables tab exactly
- Check Railway usage hasn't exceeded $5 credit

### Schema Import Failed
- Make sure you're in the correct database
- Try running SQL statements one at a time
- Check for syntax errors in `database_setup.sql`

---

## 📚 Full Guide

See `RAILWAY_DATABASE_SETUP.md` for detailed instructions!

---

**That's it!** Railway MySQL is ready to use! 🎉

