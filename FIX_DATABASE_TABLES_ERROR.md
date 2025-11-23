# Fix: "relation users does not exist" Error

## ❌ Problem:
The error `relation "users" does not exist` means the database tables haven't been created yet.

---

## ✅ Solution: Initialize Database Schema

### Step 1: Visit the Database Initialization URL

1. **Open your browser**
2. **Go to**: `https://studentcardsystem.onrender.com/init-db`
3. **Wait for the page to load** (may take 10-30 seconds)
4. **You should see**: "Database Initialization Complete!" page

---

### Step 2: Verify Tables Were Created

The page should show:
- ✅ **Tables Created:**
  - `users`
  - `student_cards`
  - `lecture_cards`
  - `support_tickets`

---

### Step 3: Test Registration Again

1. **Go to**: `https://studentcardsystem.onrender.com/register`
2. **Try creating an account again**
3. **Should work now!** ✅

---

## 🔍 If /init-db Doesn't Work:

### Check Database Connection First:

1. **Visit**: `https://studentcardsystem.onrender.com/test_db`
2. **Should show**: "Database connected! Current time: ..."
3. **If it fails** → Database connection issue (check DATABASE_URL)

---

## ⚠️ Common Issues:

### Issue 1: /init-db Shows Error
- **Check**: Is `DATABASE_URL` set in Environment variables?
- **Check**: Is database linked to web service?
- **Check**: Deployment logs for errors

### Issue 2: Tables Still Don't Exist After /init-db
- **Check**: Did you see "CREATE TABLE" messages?
- **Try**: Visit `/init-db` again (it's safe to run multiple times)
- **Check**: Deployment logs for SQL errors

---

## ✅ Quick Fix Steps:

1. ✅ Visit: `https://studentcardsystem.onrender.com/init-db`
2. ✅ Wait for "Database Initialization Complete!" message
3. ✅ Verify 4 tables are listed
4. ✅ Try registration again

---

**Visit `/init-db` now to create all tables!** 🚀

