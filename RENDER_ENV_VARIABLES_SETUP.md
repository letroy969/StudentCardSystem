# Render Environment Variables Setup

## ✅ Add These Environment Variables:

Click **"Add Environment Variable"** for each one below:

---

### 1. **FLASK_ENV**
- **Key**: `FLASK_ENV`
- **Value**: `production`
- **Click**: "Add Environment Variable"

### 2. **SECRET_KEY**
- **Key**: `SECRET_KEY`
- **Value**: Click **"Generate"** button (or use: `python -c "import secrets; print(secrets.token_hex(32))"`)
- **Click**: "Add Environment Variable"

### 3. **DATABASE_URL**
- **Key**: `DATABASE_URL`
- **Value**: **AUTO-SET** when you link PostgreSQL database (don't add manually!)
- **Status**: ✅ Already set if database is linked

### 4. **MAIL_SERVER**
- **Key**: `MAIL_SERVER`
- **Value**: `smtp.gmail.com`
- **Click**: "Add Environment Variable"

### 5. **MAIL_PORT**
- **Key**: `MAIL_PORT`
- **Value**: `587`
- **Click**: "Add Environment Variable"

### 6. **MAIL_USE_TLS**
- **Key**: `MAIL_USE_TLS`
- **Value**: `True`
- **Click**: "Add Environment Variable"

### 7. **MAIL_USERNAME**
- **Key**: `MAIL_USERNAME`
- **Value**: `umpdigitalc@gmail.com`
- **Click**: "Add Environment Variable"

### 8. **MAIL_PASSWORD**
- **Key**: `MAIL_PASSWORD`
- **Value**: `<Your 16-character Gmail App Password>`
- **Important**: Use your Gmail App Password (not regular password!)
- **Click**: "Add Environment Variable"

### 9. **MAIL_DEFAULT_SENDER**
- **Key**: `MAIL_DEFAULT_SENDER`
- **Value**: `umpdigitalc@gmail.com`
- **Click**: "Add Environment Variable"

### 10. **SUPPORT_RECIPIENT**
- **Key**: `SUPPORT_RECIPIENT`
- **Value**: `umpdigitalc@gmail.com`
- **Click**: "Add Environment Variable"

### 11. **PROFILE_BASE_URL** ⚠️
- **Key**: `PROFILE_BASE_URL`
- **Value**: `<Leave empty for now - set after first deploy>`
- **Note**: Set this AFTER your first deploy with your actual app URL
- **Click**: "Add Environment Variable" (leave value empty, or skip for now)

---

## 📋 Quick Copy-Paste List:

```
FLASK_ENV=production
SECRET_KEY=<generate-random-key>
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=umpdigitalc@gmail.com
MAIL_PASSWORD=<your-16-char-gmail-app-password>
MAIL_DEFAULT_SENDER=umpdigitalc@gmail.com
SUPPORT_RECIPIENT=umpdigitalc@gmail.com
PROFILE_BASE_URL=<set-after-deploy>
```

---

## ⚠️ Important Notes:

1. **DATABASE_URL**: Don't add manually - it's auto-set when you link PostgreSQL!

2. **SECRET_KEY**: 
   - Click "Generate" button in Render
   - OR generate locally: `python -c "import secrets; print(secrets.token_hex(32))"`

3. **MAIL_PASSWORD**: 
   - Must be Gmail App Password (16 characters)
   - NOT your regular Gmail password
   - Generate at: https://myaccount.google.com/apppasswords

4. **PROFILE_BASE_URL**: 
   - Set AFTER first deploy
   - Use your app URL: `https://your-app.onrender.com`

---

## ✅ After Adding All Variables:

1. Scroll down
2. Click **"Create Web Service"** or **"Save Changes"**
3. Wait for build to start
4. Watch build logs for any errors

---

**Add all variables above, then proceed!** 🚀

