# Verify Database Connection Setup

## ✅ Your Internal Database URL:
```
postgresql://student_card_db_qx18_user:AfUjnYEUjXf0uqxCNgHCBhee9ou8wKqC@dpg-d4gu20ili9vc73ds4jng-a/student_card_db_qx18
```

---

## 🔍 Step 1: Check if DATABASE_URL is Already Set

### Option A: Check Environment Variables
1. **Render Dashboard** → Your Web Service (`StudentCardSystem`)
2. Click **"Environment"** tab
3. Look for `DATABASE_URL` in the list
4. **If it exists** → ✅ Already set! (Render set it automatically)
5. **If it doesn't exist** → Continue to Step 2

---

## ✅ Step 2: If DATABASE_URL is NOT Set

### Add It Manually:

1. **Web Service** → **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://student_card_db_qx18_user:AfUjnYEUjXf0uqxCNgHCBhee9ou8wKqC@dpg-d4gu20ili9vc73ds4jng-a/student_card_db_qx18`
4. Click **"Save Changes"**
5. Render will **auto-redeploy**

---

## 🎯 Step 3: Verify Connection

After deployment completes:

1. Visit: `https://studentcardsystem.onrender.com/test_db`
2. Should show: **"Database connected! Current time: ..."**
3. If it works → ✅ Database connection is correct!

---

## ⚠️ Important Notes:

- **Internal URL** is correct for Render services
- **Don't share this URL** publicly (contains password)
- **Render usually sets this automatically** when database is linked
- **If manually adding**, make sure to copy the entire URL exactly

---

## ✅ Next Steps After Connection Works:

1. **Initialize Database**: Visit `https://studentcardsystem.onrender.com/init-db`
2. **Add Render Disk**: For file persistence
3. **Set PROFILE_BASE_URL**: For QR codes

---

**Check if DATABASE_URL exists in Environment variables first!** 🚀

