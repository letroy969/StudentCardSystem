# Render Web Service Setup Guide

## ⚠️ IMPORTANT: Change Settings from Node.js to Python!

The form is showing **Node.js defaults** - you need to change them to **Python/Flask**!

---

## ✅ Correct Settings for Your Flask App:

### 1. **Name**: `StudentCardSystem` ✅
   - Keep as is (or change to `ump-digital-card` if you prefer)

### 2. **Language**: Change to **Python** ⚠️
   - Currently shows: "Node"
   - **Change to**: "Python" or "Python 3"

### 3. **Branch**: Change to **master** ⚠️
   - Currently shows: "main"
   - **Change to**: "master" (your repo uses master branch)

### 4. **Build Command**: Change to **pip install** ⚠️
   - Currently shows: `yarn`
   - **Change to**: `pip install -r requirements.txt`

### 5. **Start Command**: Change to **gunicorn** ⚠️
   - Currently shows: `yarn start`
   - **Change to**: `gunicorn app:app`

### 6. **Region**: `Ohio (US East)` ✅
   - Keep as is (or change if you want same region as database)

### 7. **Root Directory**: Leave empty ✅
   - Not needed for your project

---

## 📋 Step-by-Step:

1. **Click "Language" dropdown** → Select **"Python"** or **"Python 3"**
2. **Click "Branch" dropdown** → Select **"master"**
3. **Build Command field** → Change to: `pip install -r requirements.txt`
4. **Start Command field** → Change to: `gunicorn app:app`
5. **Scroll down** → Find "Add-ons" section
6. **Link PostgreSQL Database** → Select your `student-card-db`
7. **Click "Create Web Service"**

---

## ⚠️ CRITICAL: After Creating Service

### Set Environment Variables:

Go to your service → "Environment" tab → Add these:

```
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalc@gmail.com
MAIL_PASSWORD=<your-gmail-app-password>
MAIL_DEFAULT_SENDER=umpdigitalc@gmail.com
SUPPORT_RECIPIENT=umpdigitalc@gmail.com
PROFILE_BASE_URL=<your-app-url-after-deploy>
```

**Note**: `DATABASE_URL` is auto-set when you link the database!

---

**Change those settings before clicking "Create Web Service"!** 🚀

